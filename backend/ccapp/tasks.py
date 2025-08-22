from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Contract

import os
import sys

if os.name == 'nt':  # Windows
    import msvcrt
else:  # Unix/Linux/Mac
    import fcntl

def notify_contracts_ending_tomorrow():
    tomorrow = timezone.now().date() + timedelta(days=1)
    contracts = Contract.objects.filter(end_date=tomorrow)

    for contract in contracts:
        if contract.user and contract.user.email:
            send_mail(
                subject=f"Contract ending soon: {contract.title}",
                message=f"Hello {contract.user.full_name},\n\n"
                        f"Your contract '{contract.title}' will end on {contract.end_date}.\n"
                        f"Please take necessary actions.\n\n"
                        f"Best regards,\nContract Management Team",
                from_email=None,  # will use DEFAULT_FROM_EMAIL
                recipient_list=[contract.user.email],
                fail_silently=False
            )
