import gradio as gr
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms
import modelscope_studio.components.pro as pro

with gr.Blocks() as demo, ms.Application(), antd.ConfigProvider():
    pro.WebSandbox(
        value={
            "./index.html":
            """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>روبوت خبير في الأمن السيبراني</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');

        :root {
            --primary: #3B82F6;
            --secondary: #2563EB;
            --accent: #60A5FA;
            --dark: #1F2937;
            --light: #F9FAFB;
            --success: #10B981;
            --danger: #EF4444;
            --warning: #F59E0B;
            --cyber-blue: #1E40AF;
            --cyber-red: #DC2626;
            --cyber-green: #059669;
        }

        body {
            font-family: 'Tajawal', sans-serif;
            background-color: #111827;
            min-height: 100vh;
            color: white;
        }

        .cyber-gradient {
            background: linear-gradient(135deg, var(--cyber-blue) 0%, var(--dark) 100%);
        }

        .cyber-card {
            background: rgba(30, 41, 59, 0.8);
            border-radius: 12px;
            border: 1px solid rgba(59, 130, 246, 0.3);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .cyber-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
            border-color: rgba(59, 130, 246, 0.6);
        }

        .cyber-pulse {
            animation: cyber-pulse 2s infinite;
        }

        @keyframes cyber-pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7);
            }
            70% {
                box-shadow: 0 0 0 12px rgba(59, 130, 246, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(59, 130, 246, 0);
            }
        }

        .glow-text {
            text-shadow: 0 0 10px rgba(59, 130, 246, 0.7);
        }

        .btn-glow {
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
            transition: all 0.3s ease;
        }

        .btn-glow:hover {
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.8);
            transform: translateY(-2px);
        }

        .cyber-border {
            position: relative;
            overflow: hidden;
        }

        .cyber-border::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--cyber-blue), var(--cyber-red));
        }

        .threat-level-low {
            border-left: 4px solid var(--success);
        }

        .threat-level-medium {
            border-left: 4px solid var(--warning);
        }

        .threat-level-high {
            border-left: 4px solid var(--danger);
        }

        .attack-path {
            position: relative;
            padding-left: 20px;
        }

        .attack-path::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(to bottom, var(--cyber-red), var(--cyber-blue));
        }

        .attack-step {
            position: relative;
            margin-bottom: 15px;
            padding-left: 25px;
        }

        .attack-step::before {
            content: '';
            position: absolute;
            left: 0;
            top: 8px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: var(--cyber-red);
            border: 2px solid white;
        }

        .matrix-cell {
            transition: all 0.3s ease;
        }

        .matrix-cell:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
            z-index: 10;
        }

        .network-node {
            transition: all 0.3s ease;
        }

        .network-node:hover {
            transform: scale(1.1);
            filter: drop-shadow(0 0 8px rgba(59, 130, 246, 0.7));
        }

        .cyber-terminal {
            background-color: #1E293B;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            color: #10B981;
            padding: 15px;
            height: 200px;
            overflow-y: auto;
        }

        .terminal-command {
            color: #60A5FA;
        }

        .terminal-output {
            color: #E5E7EB;
        }

        .terminal-prompt {
            color: #F59E0B;
        }

        /* Animation for cyber elements */
        @keyframes cyber-flicker {
            0%, 19.999%, 22%, 62.999%, 64%, 64.999%, 70%, 100% {
                opacity: 1;
            }
            20%, 21.999%, 63%, 63.999%, 65%, 69.999% {
                opacity: 0.4;
            }
        }

        .cyber-flicker {
            animation: cyber-flicker 3s infinite;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .cyber-card {
                padding: 15px;
            }
        }
    </style>
</head>
<body class="min-h-screen">
    <!-- Header -->
    <header class="cyber-gradient py-6 shadow-lg">
        <div class="container mx-auto px-4">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div class="flex items-center mb-4 md:mb-0">
                    <div class="cyber-gradient rounded-full p-3 mr-3 shadow-lg btn-glow">
                        <i class="fas fa-shield-halved text-2xl text-white"></i>
                    </div>
                    <h1 class="text-2xl font-bold glow-text">روبوت خبير في الأمن السيبراني</h1>
                </div>
                <div class="flex space-x-3 space-x-reverse">
                    <button class="bg-cyan-600 hover:bg-cyan-700 text-white px-4 py-2 rounded-lg btn-glow">
                        <i class="fas fa-play mr-2"></i>بدء التحليل
                    </button>
                    <button class="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg">
                        <i class="fas fa-cog mr-2"></i>الإعدادات
                    </button>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
        <!-- System Overview -->
        <section class="mb-12">
            <h2 class="text-xl font-bold mb-6 pb-2 border-b border-gray-700 flex items-center">
                <i class="fas fa-robot text-cyan-400 mr-2"></i>نظرة عامة على النظام
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <!-- Data Collection -->
                <div class="cyber-card p-6 cyber-border">
                    <div class="flex items-center mb-4">
                        <div class="bg-blue-900 rounded-full p-3 mr-3">
                            <i class="fas fa-database text-blue-300"></i>
                        </div>
                        <h3 class="font-bold text-lg">جمع البيانات</h3>
                    </div>
                    <ul class="space-y-2 text-gray-300">
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            مراقبة حركة المرور على الشبكة
                        </li>
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            جمع سجلات الأنظمة والتطبيقات
                        </li>
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            التقاط الأحداث الأمنية (SIEM)
                        </li>
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            استيراد بيانات من مصادر التهديدات
                        </li>
                    </ul>
                </div>
                
                <!-- Data Analysis -->
                <div class="cyber-card p-6 cyber-border">
                    <div class="flex items-center mb-4">
                        <div class="bg-purple-900 rounded-full p-3 mr-3">
                            <i class="fas fa-chart-line text-purple-300"></i>
                        </div>
                        <h3 class="font-bold text-lg">تحليل البيانات</h3>
                    </div>
                    <ul class="space-y-2 text-gray-300">
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            تحليل السلوك والشذوذ
                        </li>
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            التصنيف الآلي للتهديدات
                        </li>
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            تحليل الضعف البنيوي
                        </li>
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            نمذجة أنماط الهجوم
                        </li>
                    </ul>
                </div>
                
                <!-- Scenario Generation -->
                <div class="cyber-card p-6 cyber-border">
                    <div class="flex items-center mb-4">
                        <div class="bg-red-900 rounded-full p-3 mr-3">
                            <i class="fas fa-bug text-red-300"></i>
                        </div>
                        <h3 class="font-bold text-lg">توليد السيناريوهات</h3>
                    </div>
                    <ul class="space-y-2 text-gray-300">
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            محاكاة الهجمات الواقعية
                        </li>
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            نمذجة سلسلة الهجوم (Kill Chain)
                        </li>
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            نماذج MITRE ATT&CK
                        </li>
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            تقارير تقييم المخاطر
                        </li>
                    </ul>
                </div>
                
                <!-- Learning & Integration -->
                <div class="cyber-card p-6 cyber-border">
                    <div class="flex items-center mb-4">
                        <div class="bg-green-900 rounded-full p-3 mr-3">
                            <i class="fas fa-brain text-green-300"></i>
                        </div>
                        <h3 class="font-bold text-lg">التعلم والتكامل</h3>
                    </div>
                    <ul class="space-y-2 text-gray-300">
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            تحديث النماذج تلقائياً
                        </li>
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            التكامل مع أنظمة الحماية
                        </li>
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            قاعدة معرفية قابلة للتحديث
                        </li>
                        <li class="flex items-center">
                            <i class="fas fa-check-circle text-green-400 mr-2 text-sm"></i>
                            استجابات أمنية تلقائية
                        </li>
                    </ul>
                </div>
            </div>
        </section>

        <!-- Attack Scenario Generation -->
        <section class="mb-12">
            <h2 class="text-xl font-bold mb-6 pb-2 border-b border-gray-700 flex items-center">
                <i class="fas fa-fire text-red-400 mr-2"></i>توليد سيناريوهات الهجوم
            </h2>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Scenario Controls -->
                <div class="cyber-card p-6 lg:col-span-1">
                    <h3 class="font-bold text-lg mb-4 flex items-center">
                        <i class="fas fa-sliders text-blue-300 mr-2"></i>ضوابط السيناريو
                    </h3>
                    
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium mb-1">نوع الهجوم</label>
                            <select class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm">
                                <option>اختر نوع الهجوم...</option>
                                <option>هجوم تصيد (Phishing)</option>
                                <option>هجوم حقن SQL</option>
                                <option>هجوم DDoS</option>
                                <option>هجوم Man-in-the-Middle</option>
                                <option>هجوم حقن الأكواد</option>
                                <option>هجوم القوة الغاشمة</option>
                            </select>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium mb-1">مستوى التعقيد</label>
                            <div class="flex space-x-2 space-x-reverse">
                                <button class="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm">منخفض</button>
                                <button class="bg-yellow-600 hover:bg-yellow-700 text-white px-3 py-1 rounded text-sm">متوسط</button>
                                <button class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm">عالي</button>
                            </div>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium mb-1">نموذج الهجوم</label>
                            <select class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm">
                                <option>MITRE ATT&CK</option>
                                <option>STRIDE</option>
                                <option>Kill Chain</option>
                                <option>نموذج مخصص</option>
                            </select>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium mb-1">الهدف</label>
                            <input type="text" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm" placeholder="أدخل الهدف (مثال: خادم ويب)">
                        </div>
                        
                        <button class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg btn-glow flex items-center justify-center">
                            <i class="fas fa-bolt mr-2"></i> توليد السيناريو
                        </button>
                    </div>
                </div>
                
                <!-- Scenario Visualization -->
                <div class="cyber-card p-6 lg:col-span-2">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-bold text-lg flex items-center">
                            <i class="fas fa-project-diagram text-purple-300 mr-2"></i>تصور سيناريو الهجوم
                        </h3>
                        <div class="flex space-x-2 space-x-reverse">
                            <button class="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm">
                                <i class="fas fa-download mr-1"></i> تصدير
                            </button>
                            <button class="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm">
                                <i class="fas fa-share mr-1"></i> مشاركة
                            </button>
                        </div>
                    </div>
                    
                    <!-- Attack Path Visualization -->
                    <div class="attack-path mt-6">
                        <div class="attack-step">
                            <div class="cyber-card p-4 mb-2">
                                <div class="flex items-center">
                                    <div class="bg-red-500 rounded-full w-6 h-6 flex items-center justify-center mr-3">
                                        <span class="text-white text-xs">1</span>
                                    </div>
                                    <h4 class="font-bold">التجسس (Reconnaissance)</h4>
                                </div>
                                <p class="text-gray-400 text-sm mt-1">المهاجم يجمع معلومات عن الهدف من خلال مسح الشبكة وجمع البيانات المكشوفة.</p>
                            </div>
                        </div>
                        
                        <div class="attack-step">
                            <div class="cyber-card p-4 mb-2">
                                <div class="flex items-center">
                                    <div class="bg-red-500 rounded-full w-6 h-6 flex items-center justify-center mr-3">
                                        <span class="text-white text-xs">2</span>
                                    </div>
                                    <h4 class="font-bold">تطوير الأسلحة (Weaponization)</h4>
                                </div>
                                <p class="text-gray-400 text-sm mt-1">إنشاء حمولة خبيثة باستخدام أداة Metasploit لاستغلال ثغرة معروفة.</p>
                            </div>
                        </div>
                        
                        <div class="attack-step">
                            <div class="cyber-card p-4 mb-2">
                                <div class="flex items-center">
                                    <div class="bg-red-500 rounded-full w-6 h-6 flex items-center justify-center mr-3">
                                        <span class="text-white text-xs">3</span>
                                    </div>
                                    <h4 class="font-bold">التسليم (Delivery)</h4>
                                </div>
                                <p class="text-gray-400 text-sm mt-1">إرسال بريد إلكتروني تصيد يحتوي على رابط خبيث إلى موظفين في المؤسسة.</p>
                            </div>
                        </div>
                        
                        <div class="attack-step">
                            <div class="cyber-card p-4 mb-2">
                                <div class="flex items-center">
                                    <div class="bg-red-500 rounded-full w-6 h-6 flex items-center justify-center mr-3">
                                        <span class="text-white text-xs">4</span>
                                    </div>
                                    <h4 class="font-bold">الاستغلال (Exploitation)</h4>
                                </div>
                                <p class="text-gray-400 text-sm mt-1">تنفيذ الكود الخبيث عند نقر الضحية على الرابط، مما يؤدي إلى تنشيط جلسة عكسية.</p>
                            </div>
                        </div>
                        
                        <div class="attack-step">
                            <div class="cyber-card p-4">
                                <div class="flex items-center">
                                    <div class="bg-red-500 rounded-full w-6 h-6 flex items-center justify-center mr-3">
                                        <span class="text-white text-xs">5</span>
                                    </div>
                                    <h4 class="font-bold">التثبيت (Installation)</h4>
                                </div>
                                <p class="text-gray-400 text-sm mt-1">تثبيت باب خلفي على النظام للوصول المستمر.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- MITRE ATT&CK Matrix -->
        <section class="mb-12">
            <h2 class="text-xl font-bold mb-6 pb-2 border-b border-gray-700 flex items-center">
                <i class="fas fa-table text-green-400 mr-2"></i>مصفوفة MITRE ATT&CK
            </h2>
            
            <div class="cyber-card p-6 overflow-x-auto">
                <div class="min-w-max">
                    <table class="w-full">
                        <thead>
                            <tr>
                                <th class="px-4 py-2 text-right bg-gray-800">التكتيكات</th>
                                <th class="px-4 py-2 bg-gray-800">التجسس</th>
                                <th class="px-4 py-2 bg-gray-800">تطوير الموارد</th>
                                <th class="px-4 py-2 bg-gray-800">التسليم</th>
                                <th class="px-4 py-2 bg-gray-800">الاستغلال</th>
                                <th class="px-4 py-2 bg-gray-800">التثبيت</th>
                                <th class="px-4 py-2 bg-gray-800">التحكم والقيادة</th>
                                <th class="px-4 py-2 bg-gray-800">التنفيذ</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="px-4 py-2 bg-gray-800 font-bold">التجسس الأولي</td>
                                <td class="px-4 py-2 text-center">
                                    <div class="matrix-cell bg-red-900 text-white rounded p-1 mx-auto w-8 h-8 flex items-center justify-center">T1595</div>
                                </td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                            </tr>
                            <tr>
                                <td class="px-4 py-2 bg-gray-800 font-bold">تطوير الموارد</td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2 text-center">
                                    <div class="matrix-cell bg-red-900 text-white rounded p-1 mx-auto w-8 h-8 flex items-center justify-center">T1588</div>
                                </td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                            </tr>
                            <tr>
                                <td class="px-4 py-2 bg-gray-800 font-bold">آليات التسليم</td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2 text-center">
                                    <div class="matrix-cell bg-red-900 text-white rounded p-1 mx-auto w-8 h-8 flex items-center justify-center">T1566</div>
                                </td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                            </tr>
                            <tr>
                                <td class="px-4 py-2 bg-gray-800 font-bold">استغلال الثغرات</td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2 text-center">
                                    <div class="matrix-cell bg-red-900 text-white rounded p-1 mx-auto w-8 h-8 flex items-center justify-center">T1203</div>
                                </td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                            </tr>
                            <tr>
                                <td class="px-4 py-2 bg-gray-800 font-bold">التثبيت</td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2 text-center">
                                    <div class="matrix-cell bg-red-900 text-white rounded p-1 mx-auto w-8 h-8 flex items-center justify-center">T1219</div>
                                </td>
                                <td class="px-4 py-2"></td>
                                <td class="px-4 py-2"></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- Threat Intelligence & Recommendations -->
        <section class="mb-12">
            <h2 class="text-xl font-bold mb-6 pb-2 border-b border-gray-700 flex items-center">
                <i class="fas fa-lightbulb text-yellow-400 mr-2"></i>الاستخبارات الأمنية والتوصيات
            </h2>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Threat Intelligence -->
                <div class="cyber-card p-6 lg:col-span-1">
                    <h3 class="font-bold text-lg mb-4 flex items-center">
                        <i class="fas fa-bell text-red-400 mr-2"></i>التهديدات الحديثة
                    </h3>
                    
                    <div class="space-y-4">
                        <div class="cyber-card p-4 threat-level-high">
                            <div class="flex justify-between items-start">
                                <h4 class="font-bold">هجوم Log4j (CVE-2021-44228)</h4>
                                <span class="bg-red-600 text-white text-xs px-2 py-1 rounded">عالي الخطورة</span>
                            </div>
                            <p class="text-gray-400 text-sm mt-1">ثغرة في مكتبة Log4j تسمح بتنفيذ أكواد عن بعد.</p>
                            <div class="flex mt-2 text-xs text-gray-500">
                                <span class="mr-3"><i class="fas fa-calendar mr-1"></i> 10 ديسمبر 2021</span>
                                <span><i class="fas fa-link mr-1"></i> CVE-2021-44228</span>
                            </div>
                        </div>
                        
                        <div class="cyber-card p-4 threat-level-medium">
                            <div class="flex justify-between items-start">
                                <h4 class="font-bold">هجوم تصيد باستخدام Microsoft 365</h4>
                                <span class="bg-yellow-600 text-white text-xs px-2 py-1 rounded">متوسط الخطورة</span>
                            </div>
                            <p class="text-gray-400 text-sm mt-1">حملة تصيد تستهدف مستخدمي Office 365 لسرقة بيانات الاعتماد.</p>
                            <div class="flex mt-2 text-xs text-gray-500">
                                <span class="mr-3"><i class="fas fa-calendar mr-1"></i> 15 يناير 2023</span>
                                <span><i class="fas fa-link mr-1"></i> TA0001</span>
                            </div>
                        </div>
                        
                        <div class="cyber-card p-4 threat-level-low">
                            <div class="flex justify-between items-start">
                                <h4 class="font-bold">برمجية خبيثة جديدة في أجهزة IoT</h4>
                                <span class="bg-green-600 text-white text-xs px-2 py-1 rounded">منخفض الخطورة</span>
                            </div>
                            <p class="text-gray-400 text-sm mt-1">برمجية خبيثة تستهدف أجهزة إنترنت الأشياء ذات الحماية الضعيفة.</p>
                            <div class="flex mt-2 text-xs text-gray-500">
                                <span class="mr-3"><i class="fas fa-calendar mr-1"></i> 5 فبراير 2023</span>
                                <span><i class="fas fa-link mr-1"></i> MAL-2023-002</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Security Recommendations -->
                <div class="cyber-card p-6 lg:col-span-2">
                    <h3 class="font-bold text-lg mb-4 flex items-center">
                        <i class="fas fa-shield-alt text-blue-400 mr-2"></i>توصيات الحماية
                    </h3>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="cyber-card p-4">
                            <div class="flex items-center mb-2">
                                <div class="bg-blue-600 rounded-full w-6 h-6 flex items-center justify-center mr-3">
                                    <i class="fas fa-lock text-white text-xs"></i>
                                </div>
                                <h4 class="font-bold">تحديث الأنظمة</h4>
                            </div>
                            <p class="text-gray-400 text-sm">تأكد من تحديث جميع الأنظمة والبرامج بأحدث الإصدارات الأمنية.</p>
                        </div>
                        
                        <div class="cyber-card p-4">
                            <div class="flex items-center mb-2">
                                <div class="bg-blue-600 rounded-full w-6 h-6 flex items-center justify-center mr-3">
                                    <i class="fas fa-user-shield text-white text-xs"></i>
                                </div>
                                <h4 class="font-bold">المصادقة متعددة العوامل</h4>
                            </div>
                            <p class="text-gray-400 text-sm">تفعيل المصادقة الثنائية لجميع الحسابات المهمة.</p>
                        </div>
                        
                        <div class="cyber-card p-4">
                            <div class="flex items-center mb-2">
                                <div class="bg-blue-600 rounded-full w-6 h-6 flex items-center justify-center mr-3">
                                    <i class="fas fa-network-wired text-white text-xs"></i>
                                </div>
                                <h4 class="font-bold">تقسيم الشبكة</h4>
                            </div>
                            <p class="text-gray-400 text-sm">تطبيق مبدأ التقسيم الشبكي للحد من انتشار الهجمات.</p>
                        </div>
                        
                        <div class="cyber-card p-4">
                            <div class="flex items-center mb-2">
                                <div class="bg-blue-600 rounded-full w-6 h-6 flex items-center justify-center mr-3">
                                    <i class="fas fa-eye text-white text-xs"></i>
                                </div>
                                <h4 class="font-bold">مراقبة النشاط</h4>
                            </div>
                            <p class="text-gray-400 text-sm">تنفيذ حلول مراقبة النشاط لاكتشاف السلوكيات المشبوهة.</p>
                        </div>
                        
                        <div class="cyber-card p-4">
                            <div class="flex items-center mb-2">
                                <div class="bg-blue-600 rounded-full w-6 h-6 flex items-center justify-center mr-3">
                                    <i class="fas fa-users text-white text-xs"></i>
                                </div>
                                <h4 class="font-bold">التوعية الأمنية</h4>
                            </div>
                            <p class="text-gray-400 text-sm">تدريب الموظفين على التعرف على محاولات التصيد والهندسة الاجتماعية.</p>
                        </div>
                        
                        <div class="cyber-card p-4">
                            <div class="flex items-center mb-2">
                                <div class="bg-blue-600 rounded-full w-6 h-6 flex items-center justify-center mr-3">
                                    <i class="fas fa-history text-white text-xs"></i>
                                </div>
                                <h4 class="font-bold">نسخ احتياطية</h4>
                            </div>
                            <p class="text-gray-400 text-sm">الحفاظ على نسخ احتياطية حديثة ومعزولة عن الشبكة.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- System Integration & Terminal -->
        <section>
            <h2 class="text-xl font-bold mb-6 pb-2 border-b border-gray-700 flex items-center">
                <i class="fas fa-plug text-purple-400 mr-2"></i>التكامل مع الأنظمة
            </h2>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Integration Options -->
                <div class="cyber-card p-6 lg:col-span-1">
                    <h3 class="font-bold text-lg mb-4 flex items-center">
                        <i class="fas fa-cogs text-cyan-400 mr-2"></i>خيارات التكامل
                    </h3>
                    
                    <div class="space-y-4">
                        <div class="cyber-card p-4 flex items-center">
                            <div class="bg-gray-700 rounded-full p-2 mr-3">
                                <i class="fas fa-shield-virus text-green-400"></i>
                            </div>
                            <div>
                                <h4 class="font-bold text-sm">SIEM Integration</h4>
                                <p class="text-gray-400 text-xs">Splunk, IBM QRadar, ArcSight</p>
                            </div>
                        </div>
                        
                        <div class="cyber-card p-4 flex items-center">
                            <div class="bg-gray-700 rounded-full p-2 mr-3">
                                <i class="fas fa-fire-extinguisher text-red-400"></i>
                            </div>
                            <div>
                                <h4 class="font-bold text-sm">جدران الحماية</h4>
                                <p class="text-gray-400 text-xs">Palo Alto, Fortinet, Cisco ASA</p>
                            </div>
                        </div>
                        
                        <div class="cyber-card p-4 flex items-center">
                            <div class="bg-gray-700 rounded-full p-2 mr-3">
                                <i class="fas fa-robot text-blue-400"></i>
                            </div>
                            <div>
                                <h4 class="font-bold text-sm">أنظمة SOAR</h4>
                                <p class="text-gray-400 text-xs">Demisto, Phantom, IBM Resilient</p>
                            </div>
                        </div>
                        
                        <div class="cyber-card p-4 flex items-center">
                            <div class="bg-gray-700 rounded-full p-2 mr-3">
                                <i class="fas fa-eye text-yellow-400"></i>
                            </div>
                            <div>
                                <h4 class="font-bold text-sm">أنظمة IDS/IPS</h4>
                                <p class="text-gray-400 text-xs">Snort, Suricata, Cisco Firepower</p>
                            </div>
                        </div>
                        
                        <button class="w-full bg-gray-700 hover:bg-gray-600 text-white py-2 rounded-lg flex items-center justify-center mt-4">
                            <i class="fas fa-plus-circle mr-2"></i> إضافة تكامل جديد
                        </button>
                    </div>
                </div>
                
                <!-- System Terminal -->
                <div class="cyber-card p-6 lg:col-span-2">
                    <h3 class="font-bold text-lg mb-4 flex items-center">
                        <i class="fas fa-terminal text-green-400 mr-2"></i>نظام التحكم
                    </h3>
                    
                    <div class="cyber-terminal">
                        <div class="mb-2">
                            <span class="terminal-prompt">cyberbot@security:~$</span> <span class="terminal-command">analyze --target 192.168.1.100 --profile phishing</span>
                        </div>
                        <div class="terminal-output mb-2">
                            [INFO] Starting analysis for target: 192.168.1.100<br>
                            [INFO] Loading phishing attack profile...<br>
                            [INFO] Scanning for vulnerable services...<br>
                            [WARNING] Detected outdated Exchange Server (CVE-2021-26855)<br>
                            [ALERT] Potential phishing entry point detected on port 443<br>
                        </div>
                        
                        <div class="mb-2">
                            <span class="terminal-prompt">cyberbot@security:~$</span> <span class="terminal-command">generate --scenario mitre --tactic initial_access</span>
                        </div>
                        <div class="terminal-output mb-2">
                            [INFO] Generating attack scenario using MITRE ATT&CK framework<br>
                            [INFO] Focused on tactic: Initial Access (TA0001)<br>
                            [SUCCESS] Scenario generated:<br>
                            &nbsp;&nbsp;1. Spearphishing Link (T1566.002)<br>
                            &nbsp;&nbsp;2. Exploit Public-Facing Application (T1190)<br>
                            &nbsp;&nbsp;3. Valid Accounts (T1078)<br>
                        </div>
                        
                        <div class="mb-2">
                            <span class="terminal-prompt">cyberbot@security:~$</span> <span class="terminal-command">recommend --severity high</span>
                        </div>
                        <div class="terminal-output">
                            [INFO] Generating high severity recommendations:<br>
                            &nbsp;&nbsp;1. Implement email filtering for phishing attempts<br>
                            &nbsp;&nbsp;2. Patch Exchange Server immediately<br>
                            &nbsp;&nbsp;3. Enforce MFA for all user accounts<br>
                            &nbsp;&nbsp;4. Conduct employee security awareness training<br>
                        </div>
                        
                        <div class="mt-4">
                            <span class="terminal-prompt">cyberbot@security:~$</span> <span class="terminal-command blink">|</span>
                        </div>
                    </div>
                    
                    <div class="mt-4 flex space-x-2 space-x-reverse">
                        <button class="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm">
                            <i class="fas fa-play mr-1"></i> تنفيذ
                        </button>
                        <button class="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm">
                            <i class="fas fa-stop mr-1"></i> إيقاف
                        </button>
                        <button class="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm">
                            <i class="fas fa-save mr-1"></i> حفظ
                        </button>
                        <button class="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm">
                            <i class="fas fa-trash mr-1"></i> مسح
                        </button>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 py-6 mt-12">
        <div class="container mx-auto px-4">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div class="mb-4 md:mb-0">
                    <p class="text-gray-400 text-sm">
                        <i class="fas fa-shield-alt mr-1"></i> نظام روبوت الأمن السيبراني - الإصدار 1.0.0
                    </p>
                </div>
                <div class="flex space-x-4 space-x-reverse">
                    <a href="#" class="text-gray-400 hover:text-white">
                        <i class="fab fa-github"></i>
                    </a>
                    <a href="#" class="text-gray-400 hover:text-white">
                        <i class="fab fa-twitter"></i>
                    </a>
                    <a href="#" class="text-gray-400 hover:text-white">
                        <i class="fab fa-linkedin"></i>
                    </a>
                    <a href="#" class="text-gray-400 hover:text-white">
                        <i class="fas fa-envelope"></i>
                    </a>
                </div>
            </div>
            <div class="mt-4 pt-4 border-t border-gray-800 text-center">
                <p class="text-gray-500 text-xs">
                    © 2025 فريق الأمن السيبراني. جميع الحقوق محفوظة.
                    <span class="mx-2">|</span>
                    <a href="#" class="hover:text-gray-300">سياسة الخصوصية</a>
                    <span class="mx-2">|</span>
                    <a href="#" class="hover:text-gray-300">شروط الاستخدام</a>
                </p>
            </div>
        </div>
    </footer>

    <script>
        // Simulate terminal typing effect
        document.addEventListener('DOMContentLoaded', function() {
            // Add blinking cursor effect
            setInterval(() => {
                const cursor = document.querySelector('.blink');
                if (cursor) {
                    cursor.style.visibility = (cursor.style.visibility === 'hidden' ? '' : 'hidden');
                }
            }, 500);

            // Add hover effects to cyber cards
            const cyberCards = document.querySelectorAll('.cyber-card');
            cyberCards.forEach(card => {
                card.addEventListener('mouseenter', () => {
                    card.style.transform = 'translateY(-5px)';
                });
                card.addEventListener('mouseleave', () => {
                    card.style.transform = '';
                });
            });

            // Simulate network nodes animation
            const networkNodes = document.querySelectorAll('.network-node');
            networkNodes.forEach((node, index) => {
                node.style.animationDelay = `${index * 0.2}s`;
            });

            // Toggle MITRE ATT&CK technique details
            const matrixCells = document.querySelectorAll('.matrix-cell');
            matrixCells.forEach(cell => {
                cell.addEventListener('click', () => {
                    alert(`تفاصيل تقنية MITRE ATT&CK: ${cell.textContent}\nسيتم عرض المزيد من التفاصيل في لوحة المعلومات.`);
                });
            });
        });
    </script>
</body>
</html>"""
        },
        template="html",
        height=600,
    )

