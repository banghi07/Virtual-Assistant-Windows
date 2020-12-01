from google_trans_new import google_translator

trans = google_translator()
text = trans.translate("usage", lang_tgt="vi")
print(text)