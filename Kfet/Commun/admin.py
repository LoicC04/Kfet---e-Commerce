from Kfet.Commun.models import *
from django.contrib import admin


admin.site.register(Produit)
admin.site.register(Menu)
admin.site.register(Categorie)
admin.site.register(Commentaire)
admin.site.register(Promo)
admin.site.register(TypeMenu)

def response_change(self, request, obj, *args, **kwargs):
    if request.REQUEST.has_key('_popup'):
             return HttpResponse('''                                                                                         
                <script type="text/javascript">                                                                              
                 opener.dismissAddAnotherPopup(window);                                                                      
                </script>''')
    else:
            return super(CustomModelAdmin, self).response_change(request, obj, *args, **kwargs)
