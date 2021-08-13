tag_list = []

$('#add-tag').click(function () {
    let div = $('<div class="row rounded mt-3" style="width: 100%;max-height: 100px"></div>').appendTo('#tags');
    let tag = $('<input type="text" class="rounded ml-3 mr-3" placeholder="نام تگ" required>').appendTo(div)
    $(tag).change(function () {
        tag_list.push($(tag).val())
    })
})

$('#newUser').click(function (){
    $('#all-tags').val(JSON.stringify(tag_list));
})
