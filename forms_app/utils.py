"""
Utility to forward submitted treatment requests to the receiving Django project.
Configure INITIATIVE_API_URL and INITIATIVE_API_TOKEN in settings.py.
"""
import json
import logging
import urllib.request
import urllib.error

from django.conf import settings

logger = logging.getLogger(__name__)


def send_to_receiver(treatment_request):
    """
    POST a TreatmentRequest instance to the receiving Django project's API.
    Returns True on success, False on failure.
    """
    api_url = getattr(settings, 'INITIATIVE_API_URL', None)
    api_token = getattr(settings, 'INITIATIVE_API_TOKEN', '')

    if not api_url:
        logger.warning('INITIATIVE_API_URL not configured — skipping external send.')
        return False

    payload = {
        'full_name': treatment_request.full_name,
        'phone': treatment_request.phone,
        'id_number': treatment_request.id_number,
        'birth_date': treatment_request.birth_date.isoformat(),
        'nationality': treatment_request.nationality,
        'city': treatment_request.city,
        'service_type': treatment_request.service_type,
        'notes': treatment_request.notes,
        'created_at': treatment_request.created_at.isoformat(),
        'source_id': treatment_request.pk,
    }

    data = json.dumps(payload).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {api_token}',
    }

    req = urllib.request.Request(api_url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status in (200, 201):
                treatment_request.is_sent = True
                treatment_request.save(update_fields=['is_sent'])
                logger.info(f'TreatmentRequest #{treatment_request.pk} sent successfully.')
                return True
            else:
                logger.error(f'Receiver returned status {response.status}')
                return False
    except urllib.error.URLError as e:
        logger.error(f'Failed to send TreatmentRequest #{treatment_request.pk}: {e}')
        return False
