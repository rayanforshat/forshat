"""جلب عروض الموقع المنشورة من قاعدة بيانات نظام ميدا (meeda).

الموقع العام يقرأ «اللقطة المنشورة» التي يُحدّثها زر «تحديث البيانات في الموقع»
داخل النظام، عبر اتصال قاعدة البيانات الثاني `meeda` المعرّف في الإعدادات.
"""
import json
import logging

from django.db import connections

logger = logging.getLogger(__name__)

# اسم جدول لقطة النشر في مشروع ميدا (تطبيق initiative، نموذج OffersPublication)
_PUBLICATION_TABLE = 'initiative_offerspublication'

# ربط تصنيفات النظام بشعار (slug) وأيقونة لعرضها في الموقع
CATEGORY_MAP = {
    'الاسنان':     ('dental',      '🦷'),
    'الأسنان':     ('dental',      '🦷'),
    'الجلدية':     ('derma',       '💆'),
    'ليزر الرجال': ('laser-men',   '👨'),
    'ليزر النساء': ('laser-women', '👩'),
    'البشره':      ('skin',        '✨'),
    'البشرة':      ('skin',        '✨'),
    'ابر النضارة': ('glow',        '💧'),
    'إبر النضارة': ('glow',        '💧'),
    'البوتكس':     ('botox',       '💉'),
    'الفيلر':      ('filler',      '🧴'),
    'ديرما بن':    ('dermapen',    '🪡'),
    'ديرمابن':     ('dermapen',    '🪡'),
}


def get_published_payload():
    """يعيد قاموس اللقطة المنشورة من قاعدة بيانات ميدا، أو None عند التعذّر."""
    try:
        with connections['meeda'].cursor() as cur:
            cur.execute(
                f"SELECT payload FROM {_PUBLICATION_TABLE} ORDER BY id LIMIT 1"
            )
            row = cur.fetchone()
    except Exception as e:  # قاعدة غير متاحة / الجدول غير موجود بعد
        logger.warning('تعذّر جلب عروض الموقع من قاعدة ميدا: %s', e)
        return None

    if not row or row[0] in (None, ''):
        return None

    payload = row[0]
    if isinstance(payload, (str, bytes)):
        try:
            payload = json.loads(payload)
        except (ValueError, TypeError):
            return None
    return payload if isinstance(payload, dict) else None


def build_services_context():
    """يبني سياق صفحة الخدمات (التصنيفات + العروض) من اللقطة المنشورة."""
    payload = get_published_payload()
    categories = []
    offers = []

    if payload:
        for idx, cat in enumerate(payload.get('categories', []), start=1):
            name = (cat.get('name') or '').strip()
            slug, icon = CATEGORY_MAP.get(name, (f'cat{idx}', '🏥'))
            cat_offers = cat.get('offers', [])
            if not cat_offers:
                continue
            categories.append({'slug': slug, 'name': name, 'icon': icon})
            for o in cat_offers:
                old_price = _num(o.get('old_price'))
                new_price = _num(o.get('new_price'))
                offers.append({
                    'name': (o.get('name') or '').strip(),
                    'category_slug': slug,
                    'category_name': name,
                    'category_icon': icon,
                    'price': new_price,
                    'old_price': old_price,
                    'has_discount': bool(old_price and new_price and old_price > new_price),
                })

    return {
        'categories': categories,
        'offers': offers,
        'total_count': len(offers),
    }


def _num(value):
    try:
        f = float(value)
    except (TypeError, ValueError):
        return 0
    return int(f) if f.is_integer() else f
