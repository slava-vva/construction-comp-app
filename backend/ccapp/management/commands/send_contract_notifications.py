from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from ...models import Contract

class Command(BaseCommand):
    help = "Send email notifications 1 day before contract end date"

    def handle(self, *args, **kwargs):
        tomorrow = timezone.localdate() + timezone.timedelta(days=1)
        contracts = Contract.objects.filter(end_date=tomorrow)

        for contract in contracts:
            subject = "Contract Expiration Reminder"
            message = (
                f"Dear {contract.user.full_name},\n\n"
                f"Your contract '{contract.title}' will expire on {contract.end_date}.\n"
                f"Please take necessary action."
            )

            send_mail(
                subject,
                message,
                "slava@gmail.com",  # From
                [contract.user.email],  # To
                fail_silently=False,
            )

        self.stdout.write(self.style.SUCCESS(f"Sent {contracts.count()} reminder(s)."))
