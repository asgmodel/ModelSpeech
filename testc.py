# تأكد من تثبيت Gradio ورrequests قبل تشغيل الكود
# pip install gradio requests

import requests
import json
import random
import datetime
import sys
import logging
from typing import Dict, Any, List, Optional, Union, Tuple

import gradio as gr # استيراد مكتبة Gradio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SpecLoadError(Exception):
    """Custom exception for errors during OpenAPI spec loading."""
    pass

class TestGenerationError(Exception):
    """Custom exception for errors during request generation (body/params)."""
    pass

class ApiTester:
    """
    A class to test API endpoints defined in an OpenAPI specification.
    (Based on the provided code with improvements for error handling, config, and logging)
    """
    def __init__(self, base_url: str, spec_path: Optional[str] = None, spec_data: Optional[Dict[str, Any]] = None,
                 login_path: str = '/api/login', logout_path: str = '/api/logout', auth_token_key: str = 'accessToken'):
        """
        Initializes the ApiTester.

        Args:
            base_url: The base URL of the API (e.g., "https://your-api.com").
            spec_path: The path/URL to the OpenAPI JSON file. Can be relative to base_url or an absolute URL.
            spec_data: The loaded OpenAPI dictionary (alternative to spec_path).
            login_path: The path for the login endpoint (default: /api/Login).
            logout_path: The path for the logout endpoint (default: /api/Logout).
            auth_token_key: The key name in the login response for the access token (default: accessToken).

        Raises:
            ValueError: If neither spec_path nor spec_data is provided.
            SpecLoadError: If the OpenAPI spec cannot be loaded or parsed.
        """
        if not base_url: # Added check for base_url
            raise ValueError("base_url must be provided.")
        if not spec_path and not spec_data:
            raise ValueError("Either spec_path or spec_data must be provided.")
        if spec_path and spec_data:
             logger.warning("Both spec_path and spec_data provided. Using spec_data.")

        self.base_url = base_url.rstrip('/') # Remove trailing slash for consistent URL building
        self.login_path = login_path
        self.logout_path = logout_path
        self.auth_token_key = auth_token_key

        try:
            self.spec = self._load_spec(spec_path, spec_data)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
             # Catch lower level errors and wrap them in a consistent SpecLoadError
             raise SpecLoadError(f"Failed to load OpenAPI spec: {e}") from e
        except SpecLoadError:
             # If _load_spec itself raised SpecLoadError, re-raise it
             raise


        self.token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.results: Dict[str, Dict[str, Any]] = {} # Store results in { operation_id or method_path : Dict for row }

    def _load_spec(self, spec_path: Optional[str], spec_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Loads the OpenAPI specification from file path (local or URL) or data."""
        if spec_data:
            logger.info("Using provided spec data.")
            return spec_data
        elif spec_path:
            try:
                logger.info(f"Attempting to load spec from direct path/URL: {spec_path}...")
                if spec_path.startswith('http://') or spec_path.startswith('https://'):
                    response = requests.get(spec_path, timeout=10)
                    response.raise_for_status()
                    loaded_spec = response.json()
                else: # Assume local file path
                    with open(spec_path, 'r', encoding='utf-8') as f:
                        loaded_spec = json.load(f)
                logger.info("Spec loaded successfully from direct path/URL.")
                return loaded_spec
            except (requests.exceptions.RequestException, json.JSONDecodeError, FileNotFoundError, OSError) as e:
                logger.warning(f"Could not load spec from direct path/URL ({spec_path}): {e}. Attempting relative to base_url...")
                try:
                    relative_spec_path = spec_path if spec_path.startswith('/') else '/' + spec_path
                    full_spec_url = f"{self.base_url}{relative_spec_path}"
                    logger.info(f"Attempting to load spec from relative path: {full_spec_url}...")
                    response = requests.get(full_spec_url, timeout=10)
                    response.raise_for_status()
                    loaded_spec = response.json()
                    logger.info("Spec loaded successfully from relative path.")
                    return loaded_spec
                except (requests.exceptions.RequestException, json.JSONDecodeError) as e_rel:
                     raise SpecLoadError(f"Failed to load spec from '{spec_path}' (direct) or '{full_spec_url}' (relative): {e_rel}") from e_rel
        else:
             raise SpecLoadError("No spec source provided to _load_spec.")


    def _resolve_ref(self, schema: Dict[str, Any], visited_refs: Optional[set] = None) -> Dict[str, Any]:
        """Resolves a JSON schema $ref. Handles basic internal refs and potential cycles."""
        if visited_refs is None:
            visited_refs = set()

        if '$ref' not in schema:
            return schema

        ref = schema['$ref']
        if ref in visited_refs:
            logger.warning(f"Detected potential reference cycle or duplicate resolution for ref: {ref}. Returning empty object.")
            return {}

        visited_refs.add(ref)

        parts = ref.split('/')
        if parts[0] == '#' and parts[1] == 'components' and parts[2] == 'schemas' and len(parts) == 4:
            schema_name = parts[-1]
            resolved_schema = self.spec.get('components', {}).get('schemas', {}).get(schema_name)
            if not resolved_schema:
                logger.warning(f"Could not resolve $ref: {ref}. Schema '{schema_name}' not found.")
                return {}
            return self._resolve_ref(resolved_schema, visited_refs.copy())
        else:
            logger.warning(f"Unhandled $ref format or location: {ref}. Only '#/components/schemas/' is fully supported.")
            return {}

    def _get_example_value(self, schema: Dict[str, Any]) -> Any:
        if 'example' in schema:
            return schema['example']
        if 'default' in schema:
            return schema['default']

        if '$ref' in schema:
            resolved_schema = self._resolve_ref(schema)
            if not resolved_schema or '$ref' in resolved_schema:
                 logger.warning(f"Failed to resolve schema for $ref: {schema.get('$ref')}. Cannot generate example.")
                 return None
            return self._get_example_value(resolved_schema)

        if 'enum' in schema and schema['enum']:
            return random.choice(schema['enum'])

        schema_type = schema.get('type')
        schema_format = schema.get('format')
        properties = schema.get('properties')
        items = schema.get('items')
        required_fields = schema.get('required', [])

        if schema_type == 'string':
            if schema_format == 'email': return 'testuser@example.com'
            if schema_format == 'password': return 'P@$$wOrd123'
            if schema_format == 'date-time': return datetime.datetime.now(datetime.timezone.utc).isoformat()
            if schema_format == 'date': return datetime.date.today().isoformat()
            if schema_format == 'uuid': return "123e4567-e89b-12d3-a456-426614174000"
            if schema_format in ('binary', 'byte'): return "base64placeholder"
            if schema_format == 'int64': return "9876543210987654321"
            min_length = schema.get('minLength', 1) # Ensure at least 1 character for generic strings
            max_length = schema.get('maxLength', 50)
            base = f'{schema_format or schema_type or "value"}'
            generated = (base * ((min_length // len(base)) + 1 if len(base) > 0 else 1))[:max_length]
            return generated if len(generated) >= min_length else (generated + 'a' * (min_length - len(generated)))
        if schema_type == 'integer': return random.randint(0,100) # Random int for more variance
        if schema_type == 'number': return round(random.uniform(0.0, 100.0), 2) # Random float
        if schema_type == 'boolean': return random.choice([True, False]) # Random boolean
        if schema_type is None:
            if properties: schema_type = 'object'
            elif items: schema_type = 'array'

        if schema_type == 'array':
            if items:
                # Generate a small, random number of items (e.g., 0 to 2) for arrays
                num_items = random.randint(0, 2)
                example_array = []
                for _ in range(num_items):
                    item_value = self._get_example_value(items)
                    if item_value is not None:
                        example_array.append(item_value)
                return example_array
            else:
                logger.warning(f"Array schema {schema} is missing 'items'. Cannot generate example item.")
                return []
        if schema_type == 'object':
            if properties:
                example_obj = {}
                for prop_name, prop_schema in properties.items():
                     is_required = prop_name in required_fields
                     # For auto-generation, include optional fields ~50% of the time if not required
                     include_optional = random.choice([True, False])
                     if is_required or include_optional:
                        prop_value = self._get_example_value(prop_schema)
                        if prop_value is not None or is_required: # Include if value generated, or if required (even if value is None)
                            example_obj[prop_name] = prop_value
                for prop_name in required_fields:
                    if prop_name not in example_obj:
                        logger.warning(f"Failed to generate value for required property '{prop_name}'. Including None in payload.")
                        example_obj[prop_name] = None
                return example_obj
            else:
                 return {}

        if schema_type is None:
             logger.warning(f"Schema {schema} has no discernible type. Potential allOf/anyOf/oneOf complexity or missing type.")
             return None
        else:
            logger.warning(f"Unhandled schema type: {schema_type} in schema {schema}. Cannot generate example value.")
            return None


    def _generate_request_body(self, request_body_spec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        content = request_body_spec.get('content', {})
        # More robust check for JSON content types
        json_content = None
        for ct in ['application/json', 'text/json', '*/*']: # Check common types, then wildcard
            if ct in content:
                json_content = content[ct]
                break
        # Check for application/*+json last as it's more specific
        if not json_content:
            for key, value in content.items():
                if key.startswith('application/') and key.endswith('+json'):
                    json_content = value
                    break
        
        if json_content and 'schema' in json_content:
            schema = json_content['schema']
            try:
                body_data = self._get_example_value(schema)
                return body_data
            except Exception as e:
                 logger.error(f"Error during request body generation from schema {schema}: {e}", exc_info=True)
                 return None
        elif request_body_spec.get('required', False):
             logger.warning(f"Request body is marked required but no suitable JSON schema found in content types for spec: {request_body_spec}")
             return None
        else:
            logger.debug("Request body is optional or no suitable schema found. Returning None.")
            return None

    def _generate_parameters(self, parameters_spec: List[Dict[str, Any]], param_type: str) -> Dict[str, Any]:
        params = {}
        for param_spec in parameters_spec:
            if param_spec.get('in') == param_type:
                name = param_spec.get('name')
                required = param_spec.get('required', False)
                schema = param_spec.get('schema')

                if name and schema:
                    try:
                         param_value = self._get_example_value(schema)
                         if param_value is not None or required:
                            params[name] = str(param_value) if param_type == 'path' and param_value is not None else param_value
                            logger.debug(f"Generated value for {param_type} parameter '{name}': {params[name]}")
                         # If param_value is None and not required, it's skipped
                    except Exception as e:
                         logger.error(f"Error during {param_type} parameter generation for '{name}' ({schema}): {e}", exc_info=True)
                         if required:
                              params[name] = None
                elif name and required:
                     logger.error(f"Required {param_type} parameter '{name}' has no schema definition.")
                     params[name] = None
        
        final_params = {}
        for param_spec in parameters_spec:
             if param_spec.get('in') == param_type:
                  name = param_spec.get('name')
                  required = param_spec.get('required', False)
                  generated_value = params.get(name) # Use .get for safety

                  if generated_value is not None:
                       final_params[name] = generated_value
                  elif required: # If required and generation resulted in None or failed
                       final_params[name] = None # Explicitly set to None
                       logger.warning(f"{param_type.capitalize()} parameter '{name}' is required but value generation failed or yielded None.")
        return final_params


    def _build_url(self, path_template: str, path_params_values: Optional[Dict[str, str]] = None) -> str:
        url = f"{self.base_url}{path_template}"
        if path_params_values:
            for name, value in path_params_values.items():
                placeholder = f"{{{name}}}"
                if value is not None: # Only replace if value is provided
                    url = url.replace(placeholder, str(value))
                elif placeholder in url: # If param is required for template but value is None
                    logger.warning(f"Path parameter '{name}' is required for URL template '{path_template}' but value is None. URL may be invalid: {url}")
        return url


    class _ErrorResponse:
         def __init__(self, method: str, url: str, error: Exception):
              self.status_code = 0
              self.text = f"Request Failed: {error}"
              self._error = error
              try:
                   self._json_data = {"detail": self.text, "error_type": type(error).__name__}
              except Exception:
                   self._json_data = {}
              self.request = type('req', (object,), {'method': method, 'url': url, 'headers': {}})()
              self.headers = {}

         def json(self) -> Dict[str, Any]:
             return self._json_data
         def raise_for_status(self): pass


    def _make_request(self, method: str, url: str,
                      query_params: Optional[Dict[str, Any]] = None,
                      json_data: Optional[Any] = None, # Can be dict or list for JSON
                      headers: Optional[Dict[str, str]] = None) -> requests.Response:
        request_headers = {'Accept': 'application/json'}
        if json_data is not None: # Check for None, not just falsy (e.g. empty list/dict)
            request_headers['Content-Type'] = 'application/json'

        if self.token:
            request_headers['Authorization'] = f'Bearer {self.token}'
        if headers:
            request_headers.update(headers)

        filtered_query_params = {k: v for k, v in (query_params or {}).items() if v is not None}
        
        log_url = url.split('?')[0]
        logger.info(f"Making request: {method.upper()} {log_url} (Params: {list(filtered_query_params.keys()) if filtered_query_params else 'None'})")
        logger.debug(f"  Full URL: {url}")
        logger.debug(f"  Request Body Type: {type(json_data).__name__ if json_data is not None else 'None'}")
        # Be careful logging sensitive data like headers or full body
        # logger.debug(f"  Request Headers: {request_headers}") 
        # logger.debug(f"  Request Body: {json.dumps(json_data)[:200] if json_data is not None else 'None'}...")

        try:
            response = requests.request(
                method.lower(),
                url,
                params=filtered_query_params,
                json=json_data,
                headers=request_headers,
                timeout=30 # Increased timeout
            )
            logger.info(f"Received response: Status {response.status_code} for {method.upper()} {log_url}")
            # logger.debug(f"  Response Headers: {response.headers}")
            # logger.debug(f"  Response Body Snippet ({len(response.text)} chars): {response.text[:200]}...")
            return response
        except requests.exceptions.Timeout:
            logger.error(f"Request Timeout for {method.upper()} {url}", exc_info=False) # Don't need full stack for timeout usually
            return self._ErrorResponse(method, url, TimeoutError(f"Request timed out after 30s for {url}")) # type: ignore
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection Error for {method.upper()} {url}: {e}", exc_info=False)
            return self._ErrorResponse(method, url, e) # type: ignore
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Exception for {method.upper()} {url}: {e}", exc_info=True)
            return self._ErrorResponse(method, url, e) # type: ignore

    def _report_result(self, method: str, url: str, status_code: int, response_text: str, operation_id: Optional[str] = None):
        display_status = status_code if status_code != 0 else "FAIL(Request Error)"
        if status_code == 0: status_icon, outcome = '❌', 'Request Failed'
        elif 200 <= status_code < 300: status_icon, outcome = '✅', 'Success'
        elif 300 <= status_code < 400: status_icon, outcome = '⚠️', 'Redirect/Warning'
        elif status_code == 401: status_icon, outcome = '🚫', 'Unauthorized'
        elif status_code == 403: status_icon, outcome = '🛑', 'Forbidden'
        elif 400 <= status_code < 500: status_icon, outcome = '⚡️', 'Client Error'
        elif 500 <= status_code < 600: status_icon, outcome = '🚨', 'Server Error'
        else: status_icon, outcome = '❓', 'Unknown Status'

        detail = ""
        # Only try to parse JSON if it's likely JSON and an error/failure
        if (status_code >= 400 or status_code == 0) and response_text:
            try:
                error_data = json.loads(response_text)
                # Common error detail keys
                error_keys = ['detail', 'error', 'message', 'title', 'errors', 'ExceptionMessage', 'Message']
                error_parts = [str(error_data.get(k)) for k in error_keys if error_data.get(k)]
                
                # Specific handling for ASP.NET Core validation errors (often under 'errors')
                if 'errors' in error_data and isinstance(error_data['errors'], dict):
                    validation_errors = []
                    for field, messages in error_data['errors'].items():
                        if isinstance(messages, list):
                            validation_errors.append(f"{field}: {', '.join(messages)}")
                    if validation_errors:
                         error_parts.append(f"Validation: {'; '.join(validation_errors)}")
                
                error_detail_str = ", ".join(filter(None, error_parts))
                detail = f"Detail: {error_detail_str[:250]}" if error_detail_str else f"Raw: {response_text[:250]}"
                if len(error_detail_str) > 250 or len(response_text) > 250: detail += "..."

            except (json.JSONDecodeError, TypeError):
                 detail = f"Response Snippet: {response_text[:250]}{'...' if len(response_text) > 250 else ''}"
        elif response_text and (200 <= status_code < 400): # Success or redirect, show small snippet
             detail = f"Response Snippet: {response_text[:100]}{'...' if len(response_text) > 100 else ''}"


        result_key = operation_id or f"{method.upper()} {url.replace(self.base_url, '')}"
        self.results[result_key] = {
             'Key': result_key, 'Method': method.upper(), 'Path': url.replace(self.base_url, ''),
             'Status': f"{status_icon} {outcome}", 'Status Code': display_status, 'Detail': detail.strip()
        }
        # Console print for real-time feedback
        print(f"[{status_icon}] {method.upper()} {url.replace(self.base_url, '')} - Status: {display_status} {detail.strip()}")


    def test_endpoint(self, path_template: str, method: str, 
                      path_params_values: Optional[Dict[str, Any]] = None,
                      query_params: Optional[Dict[str, Any]] = None, 
                      request_body_data: Optional[Any] = None, # Can be list or dict
                      headers: Optional[Dict[str, str]] = None) -> Optional[requests.Response]:
        method_lower = method.lower()
        path_spec = self.spec.get('paths', {}).get(path_template, {})
        operation = path_spec.get(method_lower)

        op_id_for_reporting = (operation.get('operationId') if operation else None) or f"{method.upper()} {path_template}"

        if not operation:
            msg = f"Error: Endpoint {method.upper()} {path_template} not found in spec."
            logger.error(msg)
            self.results[op_id_for_reporting] = {
                 'Key': op_id_for_reporting, 'Method': method.upper(), 'Path': path_template,
                 'Status': '❌ Spec Error', 'Status Code': 'N/A', 'Detail': msg
            }
            print(f"❌ {msg}")
            return None

        operation_id = operation.get('operationId')

        # Path Parameters
        required_path_params_spec = {
            p['name'] for p in operation.get('parameters', [])
            if p.get('in') == 'path' and p.get('required', False)
        }
        effective_path_params = path_params_values or {}
        missing_required_path = [
             name for name in required_path_params_spec
             if name not in effective_path_params or effective_path_params.get(name) is None or str(effective_path_params.get(name)).strip() == ""
        ]
        if missing_required_path:
             msg = f"Missing required path parameters: {missing_required_path}. Provide concrete values."
             logger.error(f"Skipping {op_id_for_reporting}: {msg}")
             self.results[op_id_for_reporting] = {
                'Key': op_id_for_reporting, 'Method': method.upper(), 'Path': path_template,
                'Status': '⏩ Skipped', 'Status Code': 'N/A', 'Detail': msg
            }
             print(f"⏩ {msg}")
             raise ValueError(msg) # Raise error for manual test if required info is missing

        # Convert path param values to string for URL building
        string_path_params_values = {k: str(v) for k, v in effective_path_params.items() if v is not None}
        full_url = self._build_url(path_template, string_path_params_values)

        # Request Body
        body_to_send = request_body_data # Explicit data prioritized
        request_body_spec_op = operation.get('requestBody')
        if body_to_send is None and request_body_spec_op:
            try:
                generated_body = self._generate_request_body(request_body_spec_op)
                if generated_body is not None:
                    body_to_send = generated_body
                    logger.debug(f"Generated request body for {op_id_for_reporting}")
                elif request_body_spec_op.get('required', False):
                    msg = "Required request body could not be generated from spec."
                    logger.error(f"Skipping {op_id_for_reporting}: {msg}")
                    self.results[op_id_for_reporting] = {
                        'Key': op_id_for_reporting, 'Method': method.upper(), 'Path': path_template,
                        'Status': '⏩ Skipped', 'Status Code': 'N/A', 'Detail': msg
                    }
                    print(f"⏩ {msg}")
                    raise TestGenerationError(msg)
            except TestGenerationError as e: raise e
            except Exception as e:
                logger.error(f"Unexpected error generating body for {op_id_for_reporting}: {e}", exc_info=True)
                if request_body_spec_op.get('required', False):
                    msg = f"Unexpected generation error for required body: {e}"
                    # self.results[op_id_for_reporting] = { /* ... skip details ... */ }
                    print(f"⏩ {msg}")
                    raise TestGenerationError(msg) from e
        
        # Query Parameters
        query_params_to_send = query_params # Explicit data prioritized
        operation_params_spec = operation.get('parameters')
        if query_params_to_send is None and operation_params_spec:
            try:
                generated_query = self._generate_parameters(operation_params_spec, 'query')
                query_params_to_send = generated_query
                
                required_query_spec = {
                    p['name'] for p in operation_params_spec
                    if p.get('in') == 'query' and p.get('required', False)
                }
                missing_required_query = [
                    name for name in required_query_spec
                    if name not in query_params_to_send or query_params_to_send.get(name) is None
                ]
                if missing_required_query:
                    msg = f"Generation failed for required query parameters: {missing_required_query}."
                    logger.error(f"Skipping {op_id_for_reporting}: {msg}")
                    self.results[op_id_for_reporting] = {
                        'Key': op_id_for_reporting, 'Method': method.upper(), 'Path': path_template,
                        'Status': '⏩ Skipped', 'Status Code': 'N/A', 'Detail': msg
                    }
                    print(f"⏩ {msg}")
                    raise TestGenerationError(msg)
            except TestGenerationError as e: raise e
            except Exception as e:
                logger.error(f"Unexpected error generating query params for {op_id_for_reporting}: {e}", exc_info=True)
                # Check if any required query params were in spec to decide if this is critical
                if any(p.get('in') == 'query' and p.get('required', False) for p in operation_params_spec):
                    msg = f"Unexpected generation error for required query parameters: {e}"
                    # self.results[op_id_for_reporting] = { /* ... skip details ... */ }
                    print(f"⏩ {msg}")
                    raise TestGenerationError(msg) from e

        try:
             response = self._make_request(method_lower, full_url, query_params_to_send, body_to_send, headers)
             self._report_result(method_lower, full_url, response.status_code if hasattr(response, 'status_code') else 0, response.text, operation_id)
             return response
        except Exception as e: # Should be caught by _make_request, but as a safeguard
             msg = f"Unexpected error during request for {op_id_for_reporting}: {e}"
             logger.error(msg, exc_info=True)
             self.results[op_id_for_reporting] = {
                'Key': op_id_for_reporting, 'Method': method.upper(), 'Path': full_url.replace(self.base_url, ''),
                'Status': '❌ Request Error', 'Status Code': 'N/A', 'Detail': msg
            }
             print(f"❌ {msg}")
             return None

    def test_all_endpoints(self, clear_previous_results: bool = True):
        logger.info("--- Running Basic Automated Smoke Test ---")
        if clear_previous_results:
            self.results.clear()

        testable_ops_count = 0
        skipped_count = 0

        for path_template, methods in self.spec.get('paths', {}).items():
            for method, operation_spec in methods.items():
                 method_lower = method.lower()
                 operation_id = operation_spec.get('operationId')
                 result_key = operation_id or f"{method.upper()} {path_template}"

                 required_path_params = [p['name'] for p in operation_spec.get('parameters', []) if p.get('in') == 'path' and p.get('required', False)]
                 
                 skip = False
                 skip_reason = ""
                 if required_path_params:
                     skip = True
                     skip_reason = f"Requires path parameters ({', '.join(required_path_params)})"
                 # Skip methods typically requiring specific IDs or causing state changes in a simple smoke test
                 elif method_lower in ['put', 'delete', 'patch'] and '{' in path_template: # More specific skip for stateful ops on specific resources
                     skip = True
                     skip_reason = f"{method.upper()} on specific resource path usually requires known ID"
                 elif path_template in [self.login_path, self.logout_path]:
                     skip = True
                     skip_reason = f"Special auth endpoint ({path_template})"

                 if skip:
                     self.results[result_key] = {
                         'Key': result_key, 'Method': method.upper(), 'Path': path_template,
                         'Status': '⏩ Skipped', 'Status Code': 'N/A', 'Detail': skip_reason
                     }
                     # print(f"⏩ Skipping {result_key}: {skip_reason}") # _report_result will print if called
                     skipped_count += 1
                     continue # Skip to next operation

                 # If not skipped, proceed to test
                 logger.info(f"\nTesting auto-generated {result_key}")
                 testable_ops_count +=1
                 body_data = None
                 query_params_data = None
                 try:
                     if operation_spec.get('requestBody'):
                          body_data = self._generate_request_body(operation_spec['requestBody'])
                          if body_data is None and operation_spec.get('requestBody',{}).get('required', False):
                              raise TestGenerationError("Required body generation failed.")
                     if operation_spec.get('parameters'):
                          query_params_data = self._generate_parameters(operation_spec['parameters'], 'query')
                          req_q_params = {p['name'] for p in operation_spec.get('parameters',[]) if p.get('in')=='query' and p.get('required',False)}
                          missing_req_q = [name for name in req_q_params if query_params_data is None or query_params_data.get(name) is None]
                          if missing_req_q:
                              raise TestGenerationError(f"Required query params generation failed: {missing_req_q}")
                     
                     full_url = self._build_url(path_template, {}) # No path params for this auto test type
                     response = self._make_request(method_lower, full_url, query_params=query_params_data, json_data=body_data)
                     self._report_result(method_lower, full_url, response.status_code, response.text, operation_id)

                 except (TestGenerationError, ValueError) as e:
                      msg = f"Data generation/prep failed for {result_key}: {e}"
                      logger.error(msg)
                      self.results[result_key] = {
                            'Key': result_key, 'Method': method_lower.upper(), 'Path': path_template,
                            'Status': '❌ Prep Failed', 'Status Code': 'N/A', 'Detail': str(e)
                        }
                      print(f"❌ {msg}") # Console print
                 except Exception as e:
                      msg = f"Unexpected error testing {result_key}: {e}"
                      logger.error(msg, exc_info=True)
                      self.results[result_key] = {
                            'Key': result_key, 'Method': method_lower.upper(), 'Path': path_template,
                            'Status': '❌ Error', 'Status Code': 'N/A', 'Detail': str(e)
                        }
                      print(f"❌ {msg}") # Console print
        
        logger.info(f"\n--- Basic Automated Smoke Test Finished ---")
        logger.info(f"Attempted to test: {testable_ops_count}, Skipped: {skipped_count}, Total operations considered: {testable_ops_count + skipped_count}")
        return self.get_results_dataframe_format()


    def login(self, email: str, password: str, login_path_ui: str, logout_path_ui: str, auth_token_key_ui: str,
              useCookies: Optional[bool] = None, useSessionCookies: Optional[bool] = None) -> Tuple[str, Tuple[List[str], List[List[str]]]]:
        self.login_path = login_path_ui or self.login_path # Update from UI if provided
        self.logout_path = logout_path_ui or self.logout_path
        self.auth_token_key = auth_token_key_ui or self.auth_token_key

        login_op_spec = self.spec.get('paths', {}).get(self.login_path, {}).get('post')
        login_op_id = login_op_spec.get('operationId') if login_op_spec else None
        report_key = login_op_id or f"POST {self.login_path}"
        
        self.results[report_key] = {
            'Key': report_key, 'Method': 'POST', 'Path': self.login_path,
            'Status': '⏳ Attempting', 'Status Code': 'N/A', 'Detail': 'Preparing login...'
        }
        # Force immediate update for UI if possible, or rely on final return

        if not login_op_spec:
            msg = f"Login endpoint POST {self.login_path} not in spec."
            logger.error(msg)
            self.results[report_key]['Status'] = '❌ Spec Error'
            self.results[report_key]['Detail'] = msg
            return msg, self.get_results_dataframe_format()

        full_login_url = self._build_url(self.login_path)
        
        # Default login body, attempt to override with spec-generated if possible
        login_body = {'email': email, 'password': password} # Sensible default
        # Try to use schema for login body, but ensure email/password are primary
        if login_op_spec.get('requestBody'):
            try:
                generated_body = self._generate_request_body(login_op_spec['requestBody'])
                if isinstance(generated_body, dict): # Ensure it's a dict to update
                    login_body = generated_body
                    login_body['email'] = email # Override/ensure email
                    login_body['password'] = password # Override/ensure password
                # If generated_body is not a dict, or None, stick with default email/pass
            except Exception as e:
                logger.warning(f"Could not generate login body from spec: {e}. Using default email/password fields.")
        
        # Query params: Start with generated, then add explicit ones
        query_params_to_send = {}
        if login_op_spec.get('parameters'):
            try:
                generated_query = self._generate_parameters(login_op_spec['parameters'], 'query')
                query_params_to_send.update({k:v for k,v in generated_query.items() if v is not None})
            except Exception as e:
                logger.warning(f"Could not generate login query params from spec: {e}")
        
        # Add explicit params from UI, overwriting any generated if names clash
        if useCookies is not None: query_params_to_send['useCookies'] = useCookies
        if useSessionCookies is not None: query_params_to_send['useSessionCookies'] = useSessionCookies
        
        logger.debug(f"Login request body: {json.dumps(login_body)}") # Log sensitive with DEBUG
        logger.debug(f"Login query params: {query_params_to_send}")

        response = self._make_request('post', full_login_url, query_params=query_params_to_send, json_data=login_body)
        self._report_result('POST', full_login_url, response.status_code, response.text, login_op_id)

        message = "Login failed. See details."
        if 200 <= response.status_code < 300:
            try:
                data = response.json()
                if self.auth_token_key in data:
                    self.token = data[self.auth_token_key]
                    self.refresh_token = data.get('refreshToken')
                    logger.info(f"Login successful. Token key: '{self.auth_token_key}' found.")
                    message = "Login successful. Token stored."
                else:
                    message = f"Login OK (Status {response.status_code}), but token key '{self.auth_token_key}' not in response. Keys: {list(data.keys())}"
                    logger.warning(message)
                    self.token = None # Ensure token is None
            except (json.JSONDecodeError, AttributeError) as e:
                message = f"Login OK (Status {response.status_code}), but response parsing failed: {e}"
                logger.error(message, exc_info=True)
                self.token = None
        
        return message, self.get_results_dataframe_format()

    def logout(self, login_path_ui: str, logout_path_ui: str, auth_token_key_ui: str) -> Tuple[str, Tuple[List[str], List[List[str]]]]:
        self.login_path = login_path_ui or self.login_path
        self.logout_path = logout_path_ui or self.logout_path
        self.auth_token_key = auth_token_key_ui or self.auth_token_key

        logout_op_spec = self.spec.get('paths', {}).get(self.logout_path, {}).get('post') # Assuming POST
        logout_op_id = logout_op_spec.get('operationId') if logout_op_spec else None
        report_key = logout_op_id or f"POST {self.logout_path}"

        self.results[report_key] = {
            'Key': report_key, 'Method': 'POST', 'Path': self.logout_path,
            'Status': '⏳ Attempting', 'Status Code': 'N/A', 'Detail': 'Preparing logout...'
        }

        if not self.token: # Added check: if not logged in, don't attempt API logout
            msg = "Not logged in. Clearing local token (if any)."
            logger.info(msg)
            self.token = None
            self.refresh_token = None
            self.results[report_key]['Status'] = 'ℹ️ Info'
            self.results[report_key]['Detail'] = msg
            return msg, self.get_results_dataframe_format()


        if not logout_op_spec:
            msg = f"Logout endpoint POST {self.logout_path} not in spec. Clearing local token."
            logger.warning(msg) # Warning as we still clear token
            self.token = None
            self.refresh_token = None
            self.results[report_key]['Status'] = '⚠️ Spec Warning'
            self.results[report_key]['Detail'] = msg
            return msg, self.get_results_dataframe_format()

        full_logout_url = self._build_url(self.logout_path)
        logout_body = {}
        if logout_op_spec.get('requestBody'):
            try:
                generated_body = self._generate_request_body(logout_op_spec['requestBody'])
                if generated_body is not None: logout_body = generated_body
            except Exception as e:
                logger.warning(f"Could not generate logout body from spec: {e}. Using empty body.")
        
        response = self._make_request('post', full_logout_url, json_data=logout_body)
        self._report_result('POST', full_logout_url, response.status_code, response.text, logout_op_id)
        
        # Always clear local token after logout attempt
        self.token = None
        self.refresh_token = None
        logger.info("Local tokens cleared after logout attempt.")

        message = f"Logout attempt finished. Status: {response.status_code}. Local tokens cleared."
        if 200 <= response.status_code < 300:
            message = "Logout successful via API. Local tokens cleared."
        elif response.status_code >=400 :
            message = f"Logout API call failed (Status: {response.status_code}). Local tokens cleared."
        
        return message, self.get_results_dataframe_format()


    def get_results_dataframe_format(self) -> Tuple[List[str], List[List[str]]]:
        headers = ['Key', 'Method', 'Path', 'Status', 'Status Code', 'Detail']
        data = []
        # Sort by Key for consistent display order
        for key in sorted(self.results.keys()): 
            row_dict = self.results[key]
            data.append([
                row_dict.get('Key', key), row_dict.get('Method', ''), row_dict.get('Path', ''),
                row_dict.get('Status', '❓'), row_dict.get('Status Code', 'N/A'), row_dict.get('Detail', '')
            ])
        return headers, data

    def get_paths(self) -> List[str]:
        if hasattr(self, 'spec') and self.spec and 'paths' in self.spec:
            return sorted(list(self.spec['paths'].keys())) # Sort for consistent UI
        return []

    def get_methods_for_path(self, path_template: str) -> List[str]:
        if hasattr(self, 'spec') and self.spec and 'paths' in self.spec and path_template in self.spec['paths']:
             method_order = ["get", "post", "put", "patch", "delete", "head", "options", "trace"]
             available_methods = [m.lower() for m in self.spec['paths'][path_template].keys()]
             return sorted(available_methods, key=lambda x: method_order.index(x) if x in method_order else len(method_order))
        return []

    def get_path_param_names_for_endpoint(self, path_template: str, method: str) -> List[str]:
        """Gets required path parameter names for a specific endpoint."""
        names = []
        if hasattr(self, 'spec') and self.spec:
            operation = self.spec.get('paths', {}).get(path_template, {}).get(method.lower())
            if operation and 'parameters' in operation:
                for param in operation['parameters']:
                    if param.get('in') == 'path' and param.get('required', False):
                        names.append(param['name'])
        return sorted(names)


    def test_controller_endpoints(self, controller_path_prefix: str, clear_previous_results: bool = False):
        if not controller_path_prefix:
            logger.error("Controller path prefix cannot be empty.")
            # Return current results if prefix is empty, maybe with an error message prepended/appended.
            headers, data = self.get_results_dataframe_format()
            # Could add a specific error row here if desired.
            return headers, data

        if not controller_path_prefix.startswith('/'):
            controller_path_prefix = '/' + controller_path_prefix
        
        logger.info(f"--- Running Automated Test for Controller Prefix: {controller_path_prefix} ---")
        if clear_previous_results: # Option to clear results only for this controller test
            # This is tricky, as self.results is global.
            # A better approach might be to return ONLY the results for this controller test
            # and let the UI decide how to merge/display.
            # For now, we'll filter the returned results instead of clearing self.results.
            pass


        ops_for_controller_count = 0
        tested_this_run_count = 0
        
        # We will build a temporary list of results for this controller run
        controller_run_results_dict: Dict[str, Dict[str, Any]] = {}

        for path_template, methods in self.spec.get('paths', {}).items():
            if not path_template.startswith(controller_path_prefix):
                continue

            ops_for_controller_count += len(methods)

            for method, operation_spec in methods.items():
                method_lower = method.lower()
                operation_id = operation_spec.get('operationId')
                result_key = operation_id or f"{method.upper()} {path_template}"

                required_path_params = [p['name'] for p in operation_spec.get('parameters', []) if p.get('in') == 'path' and p.get('required', False)]
                
                skip = False
                skip_reason = ""
                if required_path_params:
                    skip = True
                    skip_reason = f"Requires path parameters ({', '.join(required_path_params)})"
                elif path_template in [self.login_path, self.logout_path]:
                    skip = True
                    skip_reason = f"Special auth endpoint ({path_template})"
                # Add heuristic from test_all_endpoints for PUT/DELETE/PATCH on specific resources
                elif method_lower in ['put', 'delete', 'patch'] and '{' in path_template:
                     skip = True
                     skip_reason = f"{method.upper()} on specific resource path usually requires known ID"


                if skip:
                    # Add to current run's results
                    controller_run_results_dict[result_key] = {
                         'Key': result_key, 'Method': method.upper(), 'Path': path_template,
                         'Status': '⏩ Skipped', 'Status Code': 'N/A', 'Detail': skip_reason
                    }
                    # Also update global results
                    self.results[result_key] = controller_run_results_dict[result_key]
                    print(f"⏩ Skipping {result_key} for controller test: {skip_reason}")
                    continue

                logger.info(f"\nTesting controller endpoint: {result_key}")
                tested_this_run_count +=1
                body_data = None
                query_params_data = None
                try:
                    if operation_spec.get('requestBody'):
                        body_data = self._generate_request_body(operation_spec['requestBody'])
                        if body_data is None and operation_spec.get('requestBody',{}).get('required', False):
                            raise TestGenerationError("Required body generation failed.")
                    if operation_spec.get('parameters'):
                        query_params_data = self._generate_parameters(operation_spec['parameters'], 'query')
                        req_q_params = {p['name'] for p in operation_spec.get('parameters',[]) if p.get('in')=='query' and p.get('required',False)}
                        missing_req_q = [name for name in req_q_params if query_params_data is None or query_params_data.get(name) is None]
                        if missing_req_q:
                            raise TestGenerationError(f"Required query params generation failed: {missing_req_q}")
                    
                    full_url = self._build_url(path_template, {}) # No path params
                    response = self._make_request(method_lower, full_url, query_params=query_params_data, json_data=body_data)
                    
                    # _report_result updates self.results. We want to capture this specific result.
                    self._report_result(method_lower, full_url, response.status_code, response.text, operation_id)
                    controller_run_results_dict[result_key] = self.results[result_key] # Copy to controller specific results

                except (TestGenerationError, ValueError) as e:
                    msg = f"Data generation/prep failed for {result_key}: {e}"
                    logger.error(msg)
                    res_item = {
                        'Key': result_key, 'Method': method_lower.upper(), 'Path': path_template,
                        'Status': '❌ Prep Failed', 'Status Code': 'N/A', 'Detail': str(e)
                    }
                    controller_run_results_dict[result_key] = res_item
                    self.results[result_key] = res_item # Update global
                    print(f"❌ {msg}")
                except Exception as e:
                    msg = f"Unexpected error testing {result_key}: {e}"
                    logger.error(msg, exc_info=True)
                    res_item = {
                        'Key': result_key, 'Method': method_lower.upper(), 'Path': path_template,
                        'Status': '❌ Error', 'Status Code': 'N/A', 'Detail': str(e)
                    }
                    controller_run_results_dict[result_key] = res_item
                    self.results[result_key] = res_item # Update global
                    print(f"❌ {msg}")

        logger.info(f"\n--- Automated Test for Controller {controller_path_prefix} Finished ---")
        logger.info(f"Operations matching prefix: {ops_for_controller_count}, Attempted to test: {tested_this_run_count}")

        # Format and return only the results from this controller run
        headers = ['Key', 'Method', 'Path', 'Status', 'Status Code', 'Detail']
        controller_data_list = []
        if not controller_run_results_dict and ops_for_controller_count == 0:
             # No operations even found for this prefix
            controller_data_list.append([f"No operations found for prefix: {controller_path_prefix}", "", "", "ℹ️ Info", "N/A", "Check prefix or spec."])
        else:
            for key in sorted(controller_run_results_dict.keys()):
                row_dict = controller_run_results_dict[key]
                controller_data_list.append([
                    row_dict.get('Key', key), row_dict.get('Method', ''), row_dict.get('Path', ''),
                    row_dict.get('Status', '❓'), row_dict.get('Status Code', 'N/A'), row_dict.get('Detail', '')
                ])
        
        return headers, controller_data_list


# --- Gradio UI Functions ---

# Global state for the ApiTester instance
# api_tester_instance: Optional[ApiTester] = None # Replaced by gr.State

def parse_json_input(json_string: Optional[str], default_on_error: Any = None, field_name: str = "JSON input") -> Any:
    if not json_string or json_string.strip() == "":
        return default_on_error
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid {field_name}: {e}")
        gr.Warning(f"Invalid {field_name}. Please check syntax. Details: {e}")
        # raise ValueError(f"Invalid {field_name}: {e}") # Raise to stop processing
        return "ERROR_PARSING_JSON" # Special marker to indicate parsing error

def initialize_tester_ui(base_url_ui, spec_path_ui, login_path_ui, logout_path_ui, auth_token_key_ui):
    global api_tester_instance
    if not base_url_ui or not spec_path_ui:
        return None, "Base URL and Spec Path are required.", (["No Spec Loaded"], [[]]), [], [], gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False)
    try:
        tester = ApiTester(
            base_url=base_url_ui,
            spec_path=spec_path_ui,
            login_path=login_path_ui,
            logout_path=logout_path_ui,
            auth_token_key=auth_token_key_ui
        )
        # api_tester_instance = tester # Store in global for access by other functions
        paths = tester.get_paths()
        # Initial results: just show a success message
        initial_headers, initial_data = ["Message"], [["Tester initialized successfully. Paths loaded."]]
        
        # Enable other components
        return (
            tester, 
            "Tester initialized successfully. Paths loaded.", 
            # (initial_headers, initial_data), 
            gr.update(choices=paths, value=paths[0] if paths else None, interactive=True), 
            gr.update(choices=[], value=None, interactive=False), # Methods will update on path change
            gr.update(interactive=True), # Login button
            gr.update(interactive=True), # Logout button
            gr.update(interactive=True), # Test selected endpoint button
            gr.update(interactive=True), # Test all button
            gr.update(interactive=True)  # Test controller button
        )
    except (ValueError, SpecLoadError) as e:
        logger.error(f"Initialization failed: {e}", exc_info=True)
        return None, f"Error initializing tester: {e}", (["Error"], [[str(e)]]), [], [], gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False)

def update_methods_dropdown_ui(api_tester_state, selected_path):
    if api_tester_state and selected_path:
        methods = api_tester_state.get_methods_for_path(selected_path)
        first_method = methods[0] if methods else None
        path_param_names = api_tester_state.get_path_param_names_for_endpoint(selected_path, first_method) if first_method else []
        
        # Create a user-friendly string for path parameter hint
        path_params_hint = ""
        if path_param_names:
            example_json = {name: "value" for name in path_param_names}
            path_params_hint = f"Required path parameters: {', '.join(path_param_names)}. Example JSON: {json.dumps(example_json)}"
        else:
            path_params_hint = "No path parameters required for this selection (or unable to determine)."

        return gr.update(choices=methods, value=first_method, interactive=True if methods else False), path_params_hint
    return gr.update(choices=[], value=None, interactive=False), "Select a path first."

def update_path_params_hint_ui(api_tester_state, selected_path, selected_method):
    if api_tester_state and selected_path and selected_method:
        path_param_names = api_tester_state.get_path_param_names_for_endpoint(selected_path, selected_method)
        if path_param_names:
            example_json = {name: "value" for name in path_param_names}
            return f"Required path parameters for {selected_method.upper()} {selected_path}: {', '.join(path_param_names)}. Example JSON: {json.dumps(example_json)}"
        else:
            return f"No *required* path parameters for {selected_method.upper()} {selected_path} (or defaults will be used if optional)."
    return "Select path and method to see path parameter requirements."


def login_ui(api_tester_state, email_ui, password_ui, login_path_cfg, logout_path_cfg, auth_token_key_cfg, use_cookies_ui, use_session_cookies_ui):
    if not api_tester_state:
        return "Tester not initialized.", (["Error"], [["Initialize tester first."]])
    if not email_ui or not password_ui:
        return "Email and Password are required for login.", api_tester_state.get_results_dataframe_format()
    
    status_msg, (headers, data) = api_tester_state.login(
        email_ui, password_ui, 
        login_path_cfg, logout_path_cfg, auth_token_key_cfg,
        use_cookies_ui, use_session_cookies_ui
    )
    return status_msg#, (headers, data)

def logout_ui(api_tester_state, login_path_cfg, logout_path_cfg, auth_token_key_cfg):
    if not api_tester_state:
        return "Tester not initialized.", (["Error"], [["Initialize tester first."]])
    status_msg, (headers, data) = api_tester_state.logout(login_path_cfg, logout_path_cfg, auth_token_key_cfg)
    return status_msg, (headers, data)

def test_selected_endpoint_ui(api_tester_state, path_template_ui, method_ui, path_params_json_ui, query_params_json_ui, body_json_ui, headers_json_ui):
    if not api_tester_state:
        return "Tester not initialized.", (["Error"], [["Initialize tester first."]])
    if not path_template_ui or not method_ui:
        return "Path and Method must be selected.", api_tester_state.get_results_dataframe_format()

    path_params = parse_json_input(path_params_json_ui, {}, "Path Parameters JSON")
    if path_params == "ERROR_PARSING_JSON": return "Error parsing Path Parameters JSON.", api_tester_state.get_results_dataframe_format()
    
    query_params = parse_json_input(query_params_json_ui, {}, "Query Parameters JSON")
    if query_params == "ERROR_PARSING_JSON": return "Error parsing Query Parameters JSON.", api_tester_state.get_results_dataframe_format()

    body_data = parse_json_input(body_json_ui, None, "Request Body JSON") # Can be None if empty
    if body_data == "ERROR_PARSING_JSON": return "Error parsing Request Body JSON.", api_tester_state.get_results_dataframe_format()

    custom_headers = parse_json_input(headers_json_ui, {}, "Custom Headers JSON")
    if custom_headers == "ERROR_PARSING_JSON": return "Error parsing Custom Headers JSON.", api_tester_state.get_results_dataframe_format()
    
    status_msg = f"Testing {method_ui.upper()} {path_template_ui}..."
    try:
        api_tester_state.test_endpoint(
            path_template_ui, method_ui,
            path_params_values=path_params,
            query_params=query_params,
            request_body_data=body_data,
            headers=custom_headers
        )
        status_msg = f"Test for {method_ui.upper()} {path_template_ui} complete. See results below."
    except (ValueError, TestGenerationError) as e: # Catch errors from test_endpoint like missing required params
        status_msg = f"Test setup failed for {method_ui.upper()} {path_template_ui}: {e}"
        # The error should already be in results table by test_endpoint's own reporting
        logger.error(status_msg)
    except Exception as e:
        status_msg = f"Unexpected error during test for {method_ui.upper()} {path_template_ui}: {e}"
        logger.error(status_msg, exc_info=True)
        # Manually add to results if it's a very unexpected error
        op_id = f"{method_ui.upper()} {path_template_ui}"
        api_tester_state.results[op_id] = {
            'Key': op_id, 'Method': method_ui.upper(), 'Path': path_template_ui,
            'Status': '❌ UI Error', 'Status Code': 'N/A', 'Detail': str(e)
        }

    return status_msg, api_tester_state.get_results_dataframe_format()

def test_all_endpoints_ui(api_tester_state):
    if not api_tester_state:
        return "Tester not initialized.", (["Error"], [["Initialize tester first."]])
    
    status_msg = "Running automated smoke test for all applicable endpoints..."
    headers, data = api_tester_state.test_all_endpoints(clear_previous_results=True) # Clears previous global results for this type of run
    status_msg = "Automated smoke test complete. See results below."
    return status_msg,  data


def test_controller_ui(api_tester_state, controller_prefix_ui):
    if not api_tester_state:
        return "Tester not initialized.", (["Error"], [["Initialize tester first."]])
    if not controller_prefix_ui:
        return "Controller prefix cannot be empty.", api_tester_state.get_results_dataframe_format()

    status_msg = f"Running automated test for controller prefix '{controller_prefix_ui}'..."
    # test_controller_endpoints returns only results for this run
    headers, controller_data = api_tester_state.test_controller_endpoints(controller_prefix_ui)
    
    # The UI will display these specific controller results.
    # The global api_tester_state.results will also have been updated.
    # For simplicity, we'll display only the controller-specific results from this function call.
    # If we want to show ALL results including these, we'd call api_tester_state.get_results_dataframe_format()
    
    status_msg = f"Automated test for controller prefix '{controller_prefix_ui}' complete."
    return status_msg, controller_data

def clear_results_ui(api_tester_state):
    if api_tester_state:
        api_tester_state.results.clear()
        return "Results cleared.", (['Key', 'Method', 'Path', 'Status', 'Status Code', 'Detail'], [])
    return "Tester not initialized.", (['Key', 'Method', 'Path', 'Status', 'Status Code', 'Detail'], [])


# --- Gradio Interface Definition ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    api_tester_state = gr.State(None) # To store the ApiTester instance

    gr.Markdown("# OpenAPI Endpoint Tester")
    status_output = gr.Textbox(label="Status", interactive=False)

    with gr.Tabs():
        with gr.TabItem("Configuration & Initialization"):
            gr.Markdown("## Step 1: Configure and Load API Specification")
            with gr.Row():
                base_url_input = gr.Textbox(label="Base API URL", placeholder="e.g., http://localhost:5000", value="https://lahja-api.runasp.net")
                spec_path_input = gr.Textbox(label="OpenAPI Spec Path/URL", placeholder="e.g., /swagger/v1/swagger.json or https://.../openapi.json", value="https://lahja-api.runasp.net/swagger/User/swagger.json")
            with gr.Accordion("Advanced Configuration (Login/Logout Paths, Token Key)", open=False):
                with gr.Row():
                    login_path_input = gr.Textbox(label="Login Path", value="/api/login")
                    logout_path_input = gr.Textbox(label="Logout Path", value="/api/logout")
                    auth_token_key_input = gr.Textbox(label="Auth Token Key in Response", value="accessToken")
            
            init_button = gr.Button("Load Spec & Initialize Tester", variant="primary")

        with gr.TabItem("Authentication"):
            gr.Markdown("## Step 2: Authenticate (Login/Logout)")
            with gr.Row():
                email_input = gr.Textbox(label="Email/Username",value="admin@gmail.com")
                password_input = gr.Textbox(label="Password", type="password")
            with gr.Row():
                use_cookies_checkbox = gr.Checkbox(label="Use Cookies (Login Query Param)", value=False) # Example for specific API
                use_session_cookies_checkbox = gr.Checkbox(label="Use Session Cookies (Login Query Param)", value=False) # Example
            with gr.Row():
                login_button = gr.Button("Login", interactive=False)
                logout_button = gr.Button("Logout", interactive=False)
        
        with gr.TabItem("Manual Endpoint Test"):
            gr.Markdown("## Step 3: Test a Specific Endpoint")
            with gr.Row():
                path_dropdown = gr.Dropdown(label="Select Path", choices=[], interactive=False)
                method_dropdown = gr.Dropdown(label="Select Method", choices=[], interactive=False)
            
            path_params_hint_output = gr.Markdown("Select path and method to see path parameter requirements.", elem_id="path-params-hint")
            
            with gr.Accordion("Parameters & Body (Enter as JSON)", open=True):
                path_params_json_input = gr.Textbox(label="Path Parameters (JSON)", placeholder='e.g., {"userId": 123, "itemId": "abc"}', lines=2, info="Provide key-value pairs for required path parameters.")
                query_params_json_input = gr.Textbox(label="Query Parameters (JSON)", placeholder='e.g., {"page": 1, "pageSize": 10}', lines=3)
                body_json_input = gr.Textbox(label="Request Body (JSON)", placeholder='e.g., {"name": "Test Item", "value": 42}', lines=5)
                headers_json_input = gr.Textbox(label="Custom Headers (JSON, Optional)", placeholder='e.g., {"X-Custom-Header": "value"}', lines=2)

            test_endpoint_button = gr.Button("Test Selected Endpoint", variant="primary", interactive=False)

        with gr.TabItem("Automated Tests"):
            gr.Markdown("## Step 4: Run Automated Tests")
            gr.Markdown("These tests attempt to use auto-generated data. Endpoints requiring specific path parameters are usually skipped.")
            with gr.Row():
                test_all_button = gr.Button("Test All (Auto-Generatable)", interactive=False)
            with gr.Row():
                controller_prefix_input = gr.Textbox(label="Controller Path Prefix", placeholder="e.g., /api/Users or /v1/items")
                test_controller_button = gr.Button("Test Controller Endpoints", interactive=False)

    gr.Markdown("## Test Results")
    clear_results_button = gr.Button("Clear All Results")
    results_df = gr.DataFrame(label="Results", headers=['Key', 'Method', 'Path', 'Status', 'Status Code', 'Detail'], 
                              interactive=False)

    # --- Event Handlers ---
    init_button.click(
        fn=initialize_tester_ui,
        inputs=[base_url_input, spec_path_input, login_path_input, logout_path_input, auth_token_key_input],
        outputs=[api_tester_state, status_output, path_dropdown, method_dropdown, 
                 login_button, logout_button, test_endpoint_button, test_all_button, test_controller_button]
    )

    path_dropdown.change(
        fn=update_methods_dropdown_ui,
        inputs=[api_tester_state, path_dropdown],
        outputs=[method_dropdown, path_params_hint_output]
    )
    
    method_dropdown.change(
        fn=update_path_params_hint_ui,
        inputs=[api_tester_state, path_dropdown, method_dropdown],
        outputs=[path_params_hint_output]
    )

    login_button.click(
        fn=login_ui,
        inputs=[api_tester_state, email_input, password_input, login_path_input, logout_path_input, auth_token_key_input, use_cookies_checkbox, use_session_cookies_checkbox],
        outputs=[status_output]
    )

    logout_button.click(
        fn=logout_ui,
        inputs=[api_tester_state, login_path_input, logout_path_input, auth_token_key_input],
        outputs=[status_output, results_df]
    )

    test_endpoint_button.click(
        fn=test_selected_endpoint_ui,
        inputs=[api_tester_state, path_dropdown, method_dropdown, path_params_json_input, query_params_json_input, body_json_input, headers_json_input],
        outputs=[status_output, results_df]
    )

    test_all_button.click(
        fn=test_all_endpoints_ui,
        inputs=[api_tester_state],
        outputs=[status_output, results_df]
    )
    
    test_controller_button.click(
        fn=test_controller_ui,
        inputs=[api_tester_state, controller_prefix_input],
        outputs=[status_output, results_df] # This will show only controller results
    )

    clear_results_button.click(
        fn=clear_results_ui,
        inputs=[api_tester_state],
        outputs=[status_output, results_df]
    )


    # demo.launch(show_error=True)
