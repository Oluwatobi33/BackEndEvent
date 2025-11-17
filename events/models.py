
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    qr_code = models.ImageField(blank=True, upload_to='qrcodes/')
    date = models.DateField()
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate QR code only when creating new event or if name changed
        if not self.qr_code and self.name:
            # Generate QR code
            qr = qrcode.make(self.name)
            
            # Create buffer
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            
            # Create filename
            fname = f'qr_code_{self.name.replace(" ", "_")}.png'
            
            # Save to ImageField
            self.qr_code.save(fname, File(buffer), save=False)
            buffer.close()
        
        super().save(*args, **kwargs)