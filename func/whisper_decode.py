import whisper

def whisper_decode(audio_path):
    whisper_model = "base"# 模型名称：tiny、base、small、medium、large，对应内存：1G、1G、2G、5G、12G
    model = whisper.load_model(whisper_model)

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"目标语言: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # print(result.text)
    return result.text
