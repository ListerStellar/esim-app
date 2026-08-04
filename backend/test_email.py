from email.message import EmailMessage
import base64

msg = EmailMessage()
msg.set_content("Text")
msg.add_alternative("<html><body><img src='cid:myimage'></body></html>", subtype="html")
html_part = msg.get_payload()[1]
html_part.add_related(b"fakeimagedata", maintype="image", subtype="png", cid="<myimage>")

print(msg.as_string())
