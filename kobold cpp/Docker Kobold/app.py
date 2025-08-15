import os
import subprocess

# Download KoboldCpp
print("Downloading KoboldCpp, please wait...")
subprocess.run([
    "wget", "-O", "dlfile.tmp",
    "https://kcpplinux.concedo.workers.dev"
])
os.rename("dlfile.tmp", "koboldcpp_linux")
os.chmod("koboldcpp_linux", 0o755)

# Define model URLs and settings
Model = "https://huggingface.co/KoboldAI/LLaMA2-13B-Tiefighter-GGUF/resolve/main/LLaMA2-13B-Tiefighter.Q4_K_S.gguf"
LoadLLaVAmmproj = False
LLaVAmmproj = "https://huggingface.co/koboldcpp/mmproj/resolve/main/llama-13b-mmproj-v1.5.Q4_1.gguf"
LoadImgModel = True
ImgModel = "https://huggingface.co/koboldcpp/imgmodel/resolve/main/imgmodel_ftuned_q4_0.gguf"
LoadSpeechModel = False
SpeechModel = "https://huggingface.co/koboldcpp/whisper/resolve/main/whisper-base.en-q5_1.bin"

VCommand = ""
SCommand = ""
WCommand = ""

if LoadLLaVAmmproj:
    VCommand = "--mmproj vmodel.gguf"
if LoadImgModel:
    SCommand = "--sdmodel imodel.gguf --sdthreads 4 --sdquant --sdclamped"
if LoadSpeechModel:
    WCommand = "--whispermodel wmodel.bin"

# Download models using aria2
subprocess.run(["apt-get", "update"])
subprocess.run(["apt-get", "install", "-y", "aria2"])
subprocess.run([
    "aria2c", "-x", "10", "-o", "model.gguf",
    "--summary-interval=5", "--allow-overwrite=true",
    "--file-allocation=none", Model
])

if VCommand:
    subprocess.run([
        "aria2c", "-x", "10", "-o", "vmodel.gguf",
        "--summary-interval=5", "--allow-overwrite=true",
        "--file-allocation=none", LLaVAmmproj
    ])
if SCommand:
    subprocess.run([
        "aria2c", "-x", "10", "-o", "imodel.gguf",
        "--summary-interval=5", "--allow-overwrite=true",
        "--file-allocation=none", ImgModel
    ])
if WCommand:
    subprocess.run([
        "aria2c", "-x", "10", "-o", "wmodel.bin",
        "--summary-interval=5", "--allow-overwrite=true",
        "--file-allocation=none", SpeechModel
    ])

# Run KoboldCpp
subprocess.run([
    "./koboldcpp_linux", "model.gguf", "--multiuser",
    "--usecublas", "0", "mmq", "--contextsize", "4096",
    "--gpulayers", "999", "--quiet", "--tensor_split", "1", "1",
    VCommand, SCommand, WCommand
])
