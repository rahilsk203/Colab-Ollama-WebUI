```markdown
# 🚀 Ollama WebUI on Google Colab

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rahilsk203/Colab-Ollama-WebUI/blob/main/Colab_Ollama_WebUI.ipynb)
[![GitHub Stars](https://img.shields.io/github/stars/rahilsk203/Colab-Ollama-WebUI?style=social)](https://github.com/rahilsk203/Colab-Ollama-WebUI)

Run large language models (LLMs) locally in your browser using Google Colab's GPU - **No installations required!**

![Demo](https://github.com/rahilsk203/Colab-Ollama-WebUI/raw/main/assets/demo.gif) <!-- Update with actual demo path -->

## 🌟 Features
- ✅ 1-Click Google Colab Setup
- ✅ Public Web UI via Ngrok
- ✅ Pre-configured with Deepseek-R1 8B model
- ✅ ChatGPT-like Chat Interface
- 🆓 Free GPU Acceleration

## 🚨 Important Note
**After completing setup:**
- Wait 2-3 minutes for all services to initialize
- Web UI will auto-load in Ngrok URL (see last cell output)

## ⚡ Quick Start (Colab)
1. Click the [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)] button
2. In Colab: **Runtime > Run All** (Ctrl+F9)
3. Monitor progress in cell outputs
4. **Final Step** will show your Web UI URL:
   ```text
   🌐 Your Web UI is available at: https://xxxx-xxx-xxx-xxx-xxx.ngrok-free.app
   ```

## 💻 Local Installation
```bash
git clone https://github.com/rahilsk203/Colab-Ollama-WebUI.git
cd Colab-Ollama-WebUI
pip install -r requirements.txt

# Start (requires Python 3.10+)
python run_ollama_webui.py
```

## 🔧 Troubleshooting
**Common Issues**:
1. `404 Error`/Blank Page:
   - Wait 2-3 minutes after setup completes
   - Refresh the Ngrok URL
   - Check Colab logs for service status

2. Ngrok Authentication Error:
   ```python
   # Replace with your token in last cell
   NGROK_AUTH_TOKEN = "your_token_here"
   ```

## ❓ FAQ
**Q: How long does setup take?**<br>
A: 5-8 minutes depending on Colab's GPU allocation

**Q: Can I use other models?**<br>
A: Yes! Edit `model_name` variable to:
- `llama2`
- `mistral`
- `phi3`
- [Full model list](https://ollama.ai/library)

**Q: Is this really free?**<br>
A: Yes! Colab provides free GPU tier (may require Google account)

## 📜 Credits
This project stands on the shoulders of giants:
- [Ollama](https://ollama.ai) - LLM runner
- [Open WebUI](https://github.com/open-webui) - Frontend
- [Ngrok](https://ngrok.com) - Secure tunneling

## ⚠️ Disclaimer
- Google Colab's free tier has usage limits
- LLM responses may be inaccurate - verify critical information
- Not affiliated with Ollama/OpenWebUI/Ngrok

---

**Developed with ❤️ by Rahil Sk**<br>
[![Follow on GitHub](https://img.shields.io/github/followers/rahilsk203?label=Follow%20%40rahilsk203&style=social)](https://github.com/rahilsk203)
```
