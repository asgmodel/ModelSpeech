import gradio as gr
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms
import modelscope_studio.components.pro as pro

with gr.Blocks() as demo, ms.Application(), antd.ConfigProvider():
    pro.WebSandbox(
        value={
            "./index.html":
            """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LAHJA AI - Advanced Text-to-Speech</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
        }
        
        .gradient-bg {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        }
        
        .textarea-shadow {
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.1), 0 2px 4px -1px rgba(79, 70, 229, 0.06);
        }
        
        .waveform {
            height: 60px;
            background: linear-gradient(90deg, #6366f1, #8b5cf6, #d946ef);
            opacity: 0.7;
            position: relative;
            overflow: hidden;
        }
        
        .waveform::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.2),
                transparent
            );
            animation: wave 1.5s linear infinite;
        }
        
        @keyframes wave {
            0% {
                transform: translateX(-100%);
            }
            100% {
                transform: translateX(100%);
            }
        }
        
        .audio-player {
            transition: all 0.3s ease;
        }
        
        .audio-player:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
    </style>
</head>
<body>
    <div class="min-h-screen flex flex-col">
        <!-- Header -->
        <header class="gradient-bg text-white py-6 shadow-lg">
            <div class="container mx-auto px-4">
                <div class="flex justify-between items-center">
                    <div class="flex items-center space-x-2">
                        <i class="fas fa-wave-square text-2xl"></i>
                        <h1 class="text-2xl font-bold">LAHJA AI</h1>
                    </div>
                    <div class="hidden md:flex items-center space-x-4">
                        <span class="text-sm font-medium bg-white/20 px-3 py-1 rounded-full">VITS Architecture</span>
                        <span class="text-sm font-medium bg-white/20 px-3 py-1 rounded-full">Transformers</span>
                    </div>
                </div>
                <p class="mt-2 text-sm opacity-80 max-w-2xl">
                    Advanced AI-powered text-to-speech with accent-aware synthesis using cutting-edge VITS architecture and transformer models.
                </p>
            </div>
        </header>

        <!-- Main Content -->
        <main class="flex-grow container mx-auto px-4 py-8">
            <div class="max-w-4xl mx-auto">
                <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                    <!-- Input Section -->
                    <div class="p-6 border-b border-gray-100">
                        <h2 class="text-xl font-semibold text-gray-800 mb-4">Text Input</h2>
                        <div class="relative">
                            <textarea id="textInput"
                                      class="w-full h-48 px-4 py-3 border border-gray-200 rounded-lg textarea-shadow focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition duration-200 resize-none"
                                      placeholder="Enter the text you want to convert to speech...">السلام عليكم كيف الحال اخبارك علومك وش مسوي بالله  وش الجديد  </textarea>
                            <div class="absolute bottom-3 right-3 flex items-center space-x-2">
                                <span id="charCount" class="text-xs text-gray-500">0 characters</span>
                                <button id="clearBtn" class="text-gray-400 hover:text-gray-600 transition">
                                    <i class="fas fa-times"></i>
                                </button>
                            </div>
                        </div>

                        <div class="mt-6 flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0">
                            <div class="flex items-center space-x-4">
                                <div class="flex items-center">
                                    <label for="voiceSelect" class="mr-2 text-sm font-medium text-gray-700">Voice:</label>
                                    <select id="voiceSelect" class="border border-gray-200 rounded-md px-3 py-1 text-sm focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                                        <option value="SA2">Najdi Arabic Haba v2</option>

                                        <option value="us">American English</option>
                                        <option value="SA1">Najdi Arabic Haba v1</option>

                                        <option value="SA3">Najdi Arabic AHmmed v1</option>
                                    </select>
                                </div>
                                <div class="flex items-center">
                                    <label for="speedSelect" class="mr-2 text-sm font-medium text-gray-700">Speed:</label>
                                    <select id="speedSelect" class="border border-gray-200 rounded-md px-3 py-1 text-sm focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                                        <option value="0.8">Slow</option>
                                        <option value="1.0" selected>Normal</option>
                                        <option value="1.2">Fast</option>
                                    </select>
                                </div>
                            </div>

                            <button id="generateBtn" class="gradient-bg hover:opacity-90 text-white font-medium py-2 px-6 rounded-lg shadow-md transition duration-200 flex items-center">
                                <i class="fas fa-play-circle mr-2"></i>
                                Generate Voice
                            </button>
                        </div>
                    </div>

                    <!-- Output Section -->
                    <div class="p-6">
                        <h2 class="text-xl font-semibold text-gray-800 mb-4">Generated Audio</h2>

                        <!-- Loading State -->
                        <div id="loadingState" class="hidden">
                            <div class="flex flex-col items-center justify-center py-8">
                                <div class="waveform w-full rounded-lg mb-4"></div>
                                <p class="text-gray-600 font-medium">Processing your request with LAHJA AI...</p>
                                <p class="text-sm text-gray-500 mt-1">This may take a few moments</p>
                            </div>
                        </div>

                        <!-- Audio Player -->
                        <div id="audioPlayerContainer" class="hidden">
                            <div class="audio-player bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-4 border border-gray-200">
                                <div class="flex items-center justify-between mb-3">
                                    <div class="flex items-center space-x-3">
                                        <i class="fas fa-headphones text-indigo-600 text-xl"></i>
                                        <div>
                                            <h3 class="font-medium text-gray-800">Generated Speech</h3>
                                            <p class="text-xs text-gray-500" id="audioInfo">American English • Normal speed</p>
                                        </div>
                                    </div>
                                    <button id="downloadBtn" class="text-indigo-600 hover:text-indigo-800 transition">
                                        <i class="fas fa-download"></i>
                                    </button>
                                </div>
                                <audio id="audioPlayer" controls class="w-full"></audio>
                            </div>
                        </div>

                        <!-- Empty State -->
                        <div id="emptyState" class="flex flex-col items-center justify-center py-12 text-center">
                            <i class="fas fa-comment-dots text-4xl text-gray-300 mb-4"></i>
                            <h3 class="text-lg font-medium text-gray-700">No audio generated yet</h3>
                            <p class="text-gray-500 max-w-md mt-1">Enter some text above and click "Generate Voice" to create your speech.</p>
                        </div>
                    </div>
                </div>

                <!-- Features Section -->
                <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <div class="text-indigo-600 mb-3">
                            <i class="fas fa-microchip text-2xl"></i>
                        </div>
                        <h3 class="font-semibold text-lg mb-2">VITS Architecture</h3>
                        <p class="text-gray-600 text-sm">
                            Our advanced VITS model synthesizes realistic audio waveforms directly from text with exceptional clarity and naturalness.
                        </p>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <div class="text-purple-600 mb-3">
                            <i class="fas fa-language text-2xl"></i>
                        </div>
                        <h3 class="font-semibold text-lg mb-2">Accent-Aware</h3>
                        <p class="text-gray-600 text-sm">
                            Captures local vocal characteristics and intonation patterns for authentic regional speech synthesis.
                        </p>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <div class="text-pink-600 mb-3">
                            <i class="fas fa-brain text-2xl"></i>
                        </div>
                        <h3 class="font-semibold text-lg mb-2">Transformer Models</h3>
                        <p class="text-gray-600 text-sm">
                            Deep linguistic analysis enables context-aware speech generation that reflects natural human expression.
                        </p>
                    </div>
                </div>
            </div>
        </main>

        <!-- Footer -->
        <footer class="bg-gray-50 py-6 border-t border-gray-200">
            <div class="container mx-auto px-4 text-center">
                <p class="text-gray-500 text-sm">
                    &copy; 2025 LAHJA AI. Advanced text-to-speech powered by VITS architecture and transformer models.
                </p>
            </div>
        </footer>
    </div>
 
        <script type="module">
            import {Client} from "https://cdn.jsdelivr.net/npm/@gradio/client/dist/index.min.js";

            document.addEventListener('DOMContentLoaded', async function () {
            // Connect to Gradio client (must be inside async function)
            const client = await Client.connect("wasmdashai/RunTasking");

            // DOM Elements
            const textInput = document.getElementById('textInput');
            const charCount = document.getElementById('charCount');
            const clearBtn = document.getElementById('clearBtn');
            const generateBtn = document.getElementById('generateBtn');
            const voiceSelect = document.getElementById('voiceSelect');
            const speedSelect = document.getElementById('speedSelect');
            const loadingState = document.getElementById('loadingState');
            const audioPlayerContainer = document.getElementById('audioPlayerContainer');
            const emptyState = document.getElementById('emptyState');
            const audioPlayer = document.getElementById('audioPlayer');
            const downloadBtn = document.getElementById('downloadBtn');
            const audioInfo = document.getElementById('audioInfo');

            const voiceLabels = {
                'us': 'American English',
                'SA1': 'Najdi Arabic Haba v1',
                'SA2': 'Najdi Arabic Haba v2',
                'SA3': 'Najdi Arabic AHmmed v1',
            
            };

            const voiceModels = {
                'us': 'wasmdashai/vits-en-v1',
                'SA1': 'wasmdashai/vits-ar-sa-huba-v1',
                'SA2': 'wasmdashai/vits-ar-sa-huba-v2',
                'SA3': 'wasmdashai/vits-ar-sa-A',

           
            };

            const speedLabels = {
                '0.3': 'Slow',
            '1.0': 'Normal',
            '1.2': 'Fast'
            };

            // Update character count
            textInput.addEventListener('input', function () {
                const count = textInput.value.length;
            charCount.textContent = `${count} characters`;
            clearBtn.classList.toggle('invisible', count === 0);
            });

            // Clear text input
            clearBtn.addEventListener('click', function () {
                textInput.value = '';
            charCount.textContent = '0 characters';
            clearBtn.classList.add('invisible');
            });

            // Generate voice
            generateBtn.addEventListener('click', async function () {
                const text = textInput.value.trim();
            if (!text) {
                alert('Please enter some text to convert to speech.');
            return;
                }

            const voice = voiceSelect.value;
            const speed = parseFloat(speedSelect.value);

            loadingState.classList.remove('hidden');
            audioPlayerContainer.classList.add('hidden');
            emptyState.classList.add('hidden');
                console.log("start result:", voice);

            try {
                    const result = await client.predict("/predict", {
                text: text,
                        name_model: voiceModels[voice],
            speaking_rate: 0.9
                    });
                console.log("Prediction result:", result);

            const audioUrl = result.data?.[0]?.url;
            if (!audioUrl) throw new Error("No audio URL received");
            
            audioPlayer.src = audioUrl;
            audioInfo.textContent = `${voiceLabels[voice]} • ${speedLabels[speed.toFixed(1)]} speed`;

            loadingState.classList.add('hidden');
            audioPlayerContainer.classList.remove('hidden');

                    // Auto play
                    setTimeout(() => {
                audioPlayer.play().catch(e => console.warn('Autoplay failed:', e));
                    }, 300);
                } catch (err) {
                console.error("Error during prediction:", err);
            loadingState.classList.add('hidden');
            emptyState.classList.remove('hidden');
                }
            });

            // Download audio
            downloadBtn.addEventListener('click', function () {
                if (audioPlayer.src) {
                    const a = document.createElement('a');
            a.href = audioPlayer.src;
            a.download = `lahja-ai-voice-${Date.now()}.mp3`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
                }
            });

            // Initialize char count
            textInput.dispatchEvent(new Event('input'));
        });
    </script>

</body>
</html>

"""
        },
        template="html",
        height=600,
    )
