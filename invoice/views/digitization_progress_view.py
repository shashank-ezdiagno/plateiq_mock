from django.shortcuts import render
from django.conf import settings
from ..models import Buyer, File


mock_buyer_id = "79365450-1fca-4fba-a2af-ef15d4bc606e"
def list_view(request):
    buyer_id = mock_buyer_id
    files = File.objects.filter(buyer_id=buyer_id)
    result = []
    for file in files:
        file_dict = dict(name=file.name, id=str(file.id), state=file.get_state_display)
        print(file.state)
        if file.state=="DIGITIZED":
            file_dict["invoice_id"] = str(file.invoice_set.get().id)
        result.append(file_dict)


    return render(request, 'progress.html', {
            'buyer_id': buyer_id, 'buyer_name': files[0].buyer.name, 'files': result
        })



