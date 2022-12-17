var  dataJson;
var LogPage;
var List;

var attrs = [];
var ids = [];

$(document).ready(function() {
    LogPage = $("#log")[0];
    List = $("#listPc");
    List.empty();
    $.ajax({
        cache: true,
        method: 'get',
        url: "/all_objects",
        success: function(obj) {
            dataJson = JSON.parse(obj);
            updateList();
            const ws = new WebSocket(`ws://localhost:8000/check/ws`);     
            
            ws.onmessage = function(event) {
                json_data = JSON.parse(event.data);

                for (let i = 0; i < json_data.length; i++) {
                    data = {'id': json_data[i].id, 'attr': json_data[i].attr, 'value': json_data[i].value};
                    console.log(data);
                    updatePc(data);
                }
                
            };
        },
        error: function(err){
            console.log(err)
        }
    });

});

function getListObj(data){
    console.log(data);
    var dang = data.has_problems.value == "True" ? "list-group-item-danger" : "";
    var status = data.is_occupied.value == "True" ? "Using..." : "...";
    var using = data.is_occupied.value == "True" ? ``   : ` d-none`;
    return `<li class="list-group-item d-flex justify-content-between align-items-start container-fluid ${dang}" id="pc${data.id.split(':').slice(-1)[0] }">`+
        `<div class="ms-2 me-auto">`+
            `<h4  name="pc_name">${data.name.value}</h4>`+
            `<span name="is_occupied">${status}</span>`+
        `</div>`+

        `<span name="using-icon" class="text-primary align-items-center ${using}" >`+
            `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-circle-fill" viewBox="0 0 32 32">`+
                `<circle cx="16" cy="16" r="16"></circle>`+
            `</svg>`+
        `</span>`+
    `</li>`;
}
  
function updateList(){
    for (let i = 0; i < dataJson.length; i++) {
        var li =  getListObj(dataJson[i]);
        ids.push(dataJson[i].id.split(':').slice(-1)[0] );
        List.append(li);
    }
    console.log(ids);
}



function updatePc(new_data){
    var elList = $('#pc'+new_data.id);
    let name = elList.find("[name='pc_name']")[0].innerText;
    var beginTextUpdate = name + "(id = "+ new_data.id + ") ";

    attr_value = new_data.value == "True" ? true : false;

    if (new_data.attr == "is_occupied"){
        let occupied = elList.find("[name='is_occupied']")[0];

        if (attr_value && occupied.innerText=="..."){
            occupied.innerText = "Using...";
            elList.find("[name='using-icon']").removeClass("d-none");
            LogPage.innerText += beginTextUpdate + "now is occupied\n";
        }
        else if (!attr_value && occupied.innerText=="Using..."){
            occupied.innerText = "...";
            elList.find("[name='using-icon']").addClass("d-none");
            LogPage.innerText += beginTextUpdate + "now is free\n";
        }
    }
    else{
        if (elList.hasClass("list-group-item-danger") && !attr_value){
            elList.removeClass("list-group-item-danger");
            LogPage.innerText += beginTextUpdate + "now is ok\n";
        }
        else if (!elList.hasClass("list-group-item-danger") && attr_value){
            elList.addClass("list-group-item-danger");
            LogPage.innerText += beginTextUpdate + "has problems\n";
        }
    }
}