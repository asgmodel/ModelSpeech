from enum import Enum

class RedirectType(Enum):
    INTERNAL = "internal"  # 
    EXTERNAL = "external"  # 

class BaseRedirect:
  
    def __init__(self):
        pass

    def redirect(self, data, url=None, redirect_type: RedirectType = None):
        
        if redirect_type == RedirectType.INTERNAL:
            return f"تم إعادة توجيه البيانات داخلياً: {data}"
        elif redirect_type == RedirectType.EXTERNAL:
            if not url:
                raise ValueError("يجب توفير رابط (URL) لإعادة التوجيه الخارجي!")
            return f"تم إعادة توجيهك إلى الرابط التالي: {url} مع البيانات: {data}"
        else:
            raise ValueError("نوع إعادة التوجيه غير صحيح!")

    def test_redirect(self, data, url=None, redirect_type: RedirectType = None):
        print(f"اختبار إعادة التوجيه: {redirect_type.value if redirect_type else 'غير محدد'}")
        return self.redirect(data, url, redirect_type)

  


