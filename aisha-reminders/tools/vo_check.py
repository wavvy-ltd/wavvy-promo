#!/usr/bin/env python3
"""Transcribe each voice line (LAN faster-whisper) and list gaps > 0.6 s, to catch MOSS repeats/stalls."""
import json, os, re, subprocess, uuid, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sb = json.load(open("storyboard.json"))


_M = None


def transcribe(path):
    global _M
    from faster_whisper import WhisperModel
    if _M is None:
        _M = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = _M.transcribe(path, language="en")
    return " ".join(s.text for s in segs).strip()


def transcribe_remote(path):
    b = uuid.uuid4().hex
    data = open(path, "rb").read()
    parts = [f"--{b}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\nfaster-whisper\r\n".encode(),
             f"--{b}\r\nContent-Disposition: form-data; name=\"language\"\r\n\r\nen\r\n".encode(),
             f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.wav\"\r\nContent-Type: audio/wav\r\n\r\n".encode() + data + b"\r\n",
             f"--{b}--\r\n".encode()]
    req = urllib.request.Request("http://192.168.100.204:8001/v1/audio/transcriptions", data=b"".join(parts),
                                 headers={"Content-Type": "multipart/form-data; boundary=" + b})
    return json.loads(urllib.request.urlopen(req, timeout=300).read())["text"].strip()


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " "))


for vo in sb["voice"]:
    t = transcribe(vo["src"])
    sil = subprocess.run(["ffmpeg", "-i", vo["src"], "-af", "silencedetect=n=-40dB:d=0.6", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    gaps = re.findall(r"silence_start: ([\d.]+)", sil)
    ok = len(norm(t).split()) <= len(norm(vo["text"]).split()) + 2
    print(f"{vo['id']} {vo['duration']:.2f}s gaps@{gaps} {'OK ' if ok else 'BAD'} | {t}")
