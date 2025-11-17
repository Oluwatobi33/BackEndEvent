from django.db import models
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    qr_code = models.ImageField(blank=True, upload_to='qrcodes/')
    date = models.DateField()
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate QR code only if it doesn't exist
        if not self.qr_code:
            qrcode_img = qrcode.make(self.name)
            canvas = Image.new('RGB', (qrcode_img.size[0], qrcode_img.size[1]), 'white')
            canvas.paste(qrcode_img)
            
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            
            fname = f'qr_code_{self.name.replace(" ", "_")}.png'
            self.qr_code.save(fname, ContentFile(buffer.getvalue()), save=False)
        
        super().save(*args, **kwargs)