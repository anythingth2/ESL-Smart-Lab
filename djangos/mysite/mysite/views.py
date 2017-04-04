from django.shortcuts import render,render_to_response
from django.http import HttpRequest,HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_protect
import json

# data={
#     {
#       "fullName":"Supavitch Sangsuwan0",
#       "nickName":"Field",
#       "statuc":"1D naja"
#     },{
#       "fullName":"Supavitch Sangsuwan1",
#       "nickName":"Field",
#       "statuc":"2D naja"
#     }
# }
data={"id":[{
      "fullName":"Supavitch Sangsuwan0",
      "nickName":"Field",
      "status":"1D naja"
    },{
      "fullName":"Supavitch Sangsuwan1",
      "nickName":"Field",
      "status":"2D naja"
    },{
      "fullName":"ChatChai",
      "nickName":"Chai",
      "status":"199D naja"
    }
    
    ]}
json_res=json.dumps(data)
json.dump(data,open("historyTable",'w+'))
print(json_res)
def dashboard(request):
    return render(request,'EslWeb/dashboard.html')

def controller(request):
    return render(request,'EslWeb/controller.html')

def member(request):
    return render(request,'EslWeb/member.html')

def historyTable(request):
    if(request.method == 'POST'):
        return JsonResponse(data)
