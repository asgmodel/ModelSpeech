from gradio_client import Client

def ask_ai(message ):
     client = Client("wasmdashai/T2T")

     
        

     result = client.predict(
         text=message,
         key="AIzaSyC85_3TKmiXtOpwybhSFThZdF1nGKlxU5c",
         api_name="/predict"
     )
     return result

def get_csharp_validator_template():
  return """You are a C# code generation expert specialized in creating validator classes.
Your task is to generate a new C# validator class strictly following the architectural template provided below.
Return ONLY the raw C# code for the validator class and its associated enum(s) and helper classes (like ServiceType if needed).
Do NOT include any extra text, explanations, comments outside of the generated code, or markdown formatting (```csharp / ```).
--- Validator Template Architecture ---
This is an example of the desired C# validator architecture. Replicate its structure, patterns, and conventions precisely for the new validator you are asked to generate.
// Example Enum defining validation states
public enum ServiceValidatorStates
{
    IsFound = 6200,
    IsFull,
    HasName,
    HasAbsolutePath,
    IsCreateSpace,
    IsDashboard,
    HasToken,
    HasValidModelAi,
    HasMethods,
    HasRequests,
    IsLinkedToUsers,
    HasId,
    HasModelAi,
    HasLinkedUsers,
    IsServiceModel,
    IsServiceIdsEmpty,
    IsInUserClaims,
    IsIn,
}
// Example Helper class for constant values used in validation attributes
public class ServiceType
{
    public const string Dash = ""dashboard"";
    public const string Space = ""createspace"";
    public const string Service = ""service"";
}
// The main Validator class structure to follow
// It inherits from ValidatorContext<TModel, TState> and implements ITValidator
// It uses [RegisterConditionValidator] attributes to link states to methods
// It includes a private caching field (_service) and overrides GetModel
public class ServiceValidator : ValidatorContext<Service, ServiceValidatorStates>
{
    private Service? _service;
    public ServiceValidator(IConditionChecker checker) : base(checker)
    {
    }
    protected override void InitializeConditions()
    {
    }
    // --- Validation Function Signature and DataFilter Explanation ---
    // ALL validation methods MUST follow this exact signature pattern:
    // private async Task<ConditionResult> MethodName(DataFilter<TProp, TModel> f)
    // Explanation of the DataFilter<TProp, TModel> parameter (conventionally named 'f'):
    // This object carries all necessary context into a validation method.
    // - TProp: The TYPE of the SPECIFIC piece of data or comparison value relevant to THIS validation method.
    //   For example:
    //   - For checking a 'string Name', TProp is 'string'.
    //   - For checking a 'bool IsActive', TProp is 'bool'.
    //   - For checking if a collection 'ICollection<Item>' is not empty, TProp might be 'object'.
    //   - For checking if a property equals a specific list of strings, TProp is 'List<string>'.
    // - TModel: The TYPE of the ENTIRE model object being validated (e.g., Service, User, Product). This is consistent for all validation methods within one ValidatorContext class.
    // Key properties of the 'f' (DataFilter) object:
    // - f.Share (Type: TModel?): This is the MOST IMPORTANT property. It provides access to the FULL INSTANCE of the model object currently being validated. You use f.Share?.PropertyName to access the model's data.
    // - f.Value (Type: TProp?): This holds an OPTIONAL comparison value passed INTO the validation method specifically for this rule. Its type matches TProp. Used when the validation isn't just a simple check on the property itself (like NotNullOrWhitespace) but involves comparing the property's value to something external.
    // - f.Id (Type: string?): The ID associated with the validation request, often the ID of the model object.
    //   - f.Name (Type: string?): An optional name or key associated with the validation request context.
    // Return Type: Validation methods MUST return Task<ConditionResult>.
    // - ConditionResult.ToSuccessAsync(result): Use for successful validation, passing relevant data (often f.Share or the validated property value) in 'result'.
    // - ConditionResult.ToFailureAsync(message) or ConditionResult.ToFailureAsync(result, message): Use for failed validation, providing an error message.
    // Use of Framework Components:
    // - await _checker.CheckAndResultAsync(...): Available via the base class. Use for performing CROSS-VALIDATION checks by triggering other states/validators.
    // - _injector: If available via base class or DI, use to access application-specific services or context (like user claims or database context as seen in ServiceValidator examples).
    // --- Example Validation Functions (from ServiceValidator) ---
    // Replicate the structure, signatures, and parameter usage (f.Share, f.Value, f.Id, f.Name) as shown in these examples for the new validator.
    [RegisterConditionValidator(typeof(ServiceValidatorStates), ServiceValidatorStates.IsFound, ""Service is not found"")]
    private Task<ConditionResult> ValidateId(DataFilter<string, Service> f)
    {
        bool valid = !string.IsNullOrWhiteSpace(f.Share?.Id);
        return valid ? ConditionResult.ToSuccessAsync(f.Share) : ConditionResult.ToFailureAsync(""Service is not found"");
    }
    [RegisterConditionValidator(typeof(ServiceValidatorStates), ServiceValidatorStates.HasName, ""Name is required"")]
    private Task<ConditionResult> ValidateName(DataFilter<string, Service> f)
    {
        bool valid = !string.IsNullOrWhiteSpace(f.Share?.Name);
        return valid ? ConditionResult.ToSuccessAsync(f.Share?.Name) : ConditionResult.ToFailureAsync(f.Share?.Name, ""Name is required"");
    }
    [RegisterConditionValidator(typeof(ServiceValidatorStates), ServiceValidatorStates.HasValidUrl, ""URL is invalid or missing"")]
    private Task<ConditionResult> ValidateAbsolutePath(DataFilter<string, Service> f)
    {
        bool valid = Uri.IsWellFormedUriString(f.Share?.AbsolutePath, UriKind.Absolute);
        return valid ? ConditionResult.ToSuccessAsync(f.Share?.AbsolutePath) : ConditionResult.ToFailureAsync(f.Share?.AbsolutePath, ""AbsolutePath is invalid"");
    }
    [RegisterConditionValidator(typeof(ServiceValidatorStates), ServiceValidatorStates.HasToken, ""Token cannot be empty if provided"")]
    private Task<ConditionResult> ValidateToken(DataFilter<string?, Service> f)
    {
        var token = f.Share?.Token;
        bool valid = token == null || !string.IsNullOrWhiteSpace(token);
        return valid ? ConditionResult.ToSuccessAsync(token) : ConditionResult.ToFailureAsync(""Token cannot be empty if provided"");
    }
    [RegisterConditionValidator(typeof(ServiceValidatorStates), ServiceValidatorStates.HasModelAi, ""Model AI is missing"")]
    private async Task<ConditionResult> ValidateModelAi(DataFilter<string, Service> f)
    {
        if (f.Share == null) return ConditionResult.ToFailure(null, ""Model AI is missing (Model is null)"");
        var res = await _checker.CheckAndResultAsync(ModelValidatorStates.HasService, f.Share.ModelAiId);
        if (res.Success == true)
        {
            return ConditionResult.ToSuccess(f.Share);
        }
        return ConditionResult.ToFailure(f.Share, res.Message ?? ""Related ModelAi check failed."");
    }
    [RegisterConditionValidator(typeof(ServiceValidatorStates), ServiceValidatorStates.HasMethods, ""No methods defined for service"")]
    private Task<ConditionResult> ValidateMethods(DataFilter<string, Service> f)
    {
        bool valid = f.Share?.ServiceMethods != null && f.Share.ServiceMethods.Any();
        return valid ? ConditionResult.ToSuccessAsync(f.Share?.ServiceMethods) : ConditionResult.ToFailureAsync(f.Share?.ServiceMethods, ""No methods defined for service"");
    }
    [RegisterConditionValidator(typeof(ServiceValidatorStates), ServiceValidatorStates.IsInUserClaims, ""Service is not in user claims"")]
    private Task<ConditionResult> ValidateServiceInUserClaims(DataFilter<string, Service> f)
    {
        bool valid = f.Share?.Id == f.Id;
        return valid ? ConditionResult.ToSuccessAsync(f.Id) : ConditionResult.ToFailureAsync(f.Id, ""Service is not in user claims"");
    }
    [RegisterConditionValidator(typeof(ServiceValidatorStates), ServiceValidatorStates.IsServiceIdsEmpty, ""User has no services"")]
    private Task<ConditionResult> ValidateServiceIdsEmpty(DataFilter<bool> f)
    {
        bool isEmpty = false;
        return isEmpty ? ConditionResult.ToSuccessAsync(isEmpty) : ConditionResult.ToFailureAsync(isEmpty, ""User has services"");
    }
    [RegisterConditionValidator(typeof(ServiceValidatorStates), ServiceValidatorStates.IsServiceModel, ""Not a valid service model"")]
    [RegisterConditionValidator(typeof(ServiceValidatorStates), ServiceValidatorStates.IsDashboard, ""Not a valid service model"", Value = ServiceType.Dash)]
    [RegisterConditionValidator(typeof(ServiceValidatorStates), ServiceValidatorStates.IsCreateSpace, ""Not a valid service model"", Value = ServiceType.Space)]
    private Task<ConditionResult> ValidateIsServiceType(DataFilter<string, Service> f)
    {
        if (f.Share == null && f.Value == null && f.Name == null) return Task.FromResult(ConditionResult.ToError(""Both Name and Value are null""));
        if (f.Share != null) return Task.FromResult(new ConditionResult(f.Share.AbsolutePath.Equals(f.Name ?? f.Value, StringComparison.OrdinalIgnoreCase), f.Share, $""No service found for {f.Name ?? f.Value}.""));
        bool valid = false;
        return valid ? ConditionResult.ToSuccessAsync(f.Share) : ConditionResult.ToErrorAsync($""No service found for {f.Name ?? f.Value}."");
    }
    [RegisterConditionValidator(typeof(ServiceValidatorStates), ServiceValidatorStates.IsIn, ""Not a valid service model"")]
    private Task<ConditionResult> IsServiceType(DataFilter<List<string>, Service> f)
    {
        if (f.Share == null && f.Value == null) return Task.FromResult(ConditionResult.ToError(""Both Name and Value are null""));
        if (f.Share != null) return Task.FromResult(new ConditionResult(f.Value?.Contains(f.Share.AbsolutePath) ?? false, f.Share, $""No service found for {f.Value}.""));
        bool valid = false;
        return valid ? ConditionResult.ToSuccessAsync(f.Share) : ConditionResult.ToErrorAsync($""No service found for {f.Value}."");
    }
    protected override async Task<Service?> GetModel(string? id)
    {
        if (_service != null && _service.Id == id)
            return _service;
        _service = await base.GetModel(id);
        return _service;
    }
}
"""

def generate_validator_prompt(model_name, model_structure, template_instructions):
    csharp_template_string = get_csharp_validator_template()

    prompt = f"""
Generate a C# Validator class for the model '{model_name}' with the following structure:
Model Name: {model_name}
Model Structure (C# Class Definition):
{model_structure}
Validator Template Pattern Requirements:
- The class must be named '{model_name}ValidatorContext'.
- It must inherit from 'ValidatorContext<{model_name}, {model_name}ValidatorStates>'.
- It must implement 'ITValidator'.
- It needs a constructor taking 'IConditionChecker checker'.
- Generate a public enum named '{model_name}ValidatorStates'. This enum should contain a state entry for EACH PUBLIC PROPERTY in the model structure (e.g., 'HasPropertyName').
- For EACH PUBLIC PROPERTY in the Model Structure, create a corresponding private method to perform validation.
    - The method signature should be 'private Task<ConditionResult> ValidatePropertyName(DataFilter<PropertyType, {model_name}> f)'. Use the actual PropertyType from the Model Structure.
    - Use 'async' only if 'await' is used inside the function body.
    - If the function uses 'async', the return reference must be either ConditionResult.ToFailureAsync or ToSuccessAsync.
    - If the function does NOT use 'async', the return reference must be ConditionResult.ToFailure or ToSuccess (use Task.FromResult(...) where necessary if not async).
    - Each validation method must use the '[RegisterConditionValidator(typeof({model_name}ValidatorStates), {model_name}ValidatorStates.HasPropertyName, ""Error message"")]' attribute.
    - Implement the 'GetModel' protected async method, ensuring it correctly handles caching if needed, similar to the provided template example.
    - dont remove any usespaces in code
    - If you use the res.Success condition and it is of type bool? the condition must be as follows (res.Success == true)
- Apply the following specific validation rules based on property types, as detailed in Template Instructions. Reference the pattern shown in the architecture below:
--- START C# VALIDATOR TEMPLATE ARCHITECTURE REFERENCE ---
{csharp_template_string}
--- END C# VALIDATOR TEMPLATE ARCHITECTURE REFERENCE ---
Your response MUST be ONLY the raw C# code for the '{model_name}ValidatorContext' class, including the enum, using statements (if necessary based on common patterns like AutoGenerator.Conditions), constructors, methods, and attributes. Do NOT include any surrounding text, explanations, or markdown. Ensure the output is just the C# code block.
Example Validation Logic Based on Common Types (Guideline for AI):
- string properties: Check for null or whitespace.
- string properties (potential URLs): Use Uri.TryCreate.
- bool properties: Often just check if the property exists or is default.
- Collection properties (like ICollection<Item>): Check if the collection is null or empty if required, or validate each item within the collection based on specific instructions.
Ensure all generated code adheres to the specified template pattern and the Template Instructions provided below.
Template Instructions:
{template_instructions}
"""
    return prompt



def process_validator_request(model_name, model_structure, template_instructions):
    if not model_name or not model_structure:
        return "Error: Model Name and Model Structure are required."

    try:
        generated_prompt = generate_validator_prompt(model_name, model_structure, template_instructions)
        response = ask_ai(generated_prompt).strip()

        # Handle both lowercase and uppercase ```csharp / ```C#
        for prefix in ["```csharp", "```C#"]:
            if response.startswith(prefix):
                response = response[len(prefix):].strip()
        
        if response.endswith("```"):
            response = response[:-len("```")].strip()

        return response

    except Exception as e:
        return f"Error during processing: {str(e)}"



def process_multiple_validators(model_names_str, model_structure, template_instructions):
    model_names = [name.strip() for name in model_names_str.split(",") if name.strip()]
    files_output = {}

    for model_name in model_names:
        result = process_validator_request(model_name, model_structure, template_instructions)
        files_output[model_name] = result

    return files_output

def render_outputs(model_names_str, model_structure, template_instructions):
    files = process_multiple_validators(model_names_str, model_structure, template_instructions)
    merged_output = ""
    for name, code in files.items():
        merged_output += f"#---------------#\n// {name}.Validator.cs\n{code}\n\n"
    return merged_output
