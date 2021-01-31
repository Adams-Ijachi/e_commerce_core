

// if(localStorage.getItem('cart') == null){
//     var cart = {};
//     }
//     else{
//     cart = JSON.parse(localStorage.getItem('cart'));
//     console.log(cart)
//     document.getElementById('cart-item-num').innerHTML = Object.keys(cart).length



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
//    }

// update cart counter and add cart item

const cart_backend_request = (url,productId,action, mythis) =>{
    $.ajax({
        url:url,
        type:'POST',
        data:{productId:productId,action:action}

     }).done( (response)=>{
        if( response.action === 'cart-update'){
            
            divs = document.getElementsByClassName( 'cart-item-num' );

            [].slice.call( divs ).forEach(function ( div ) {
                div.innerHTML = response.orderitem_count;
            });
            
            return response
        }
        else if ( response.action === 'cart-product-update'){
             
            if ( response.orderitem_count==0 ) {
       
               $("#checkout-btn").addClass("disabled");
            }
   


            cart_count_divs = document.getElementsByClassName( 'cart-item-num' );

            [].slice.call( cart_count_divs  ).forEach(function ( cart_count_div  ) {
                cart_count_div.innerHTML = response.orderitem_count;
            });

            
            order_total_divs = document.getElementsByClassName( 'order-total' );

            [].slice.call( order_total_divs ).forEach(function ( order_total_div ) {
                order_total_div.innerHTML = response.order_total;
            });

            var div_table_data = mythis.parents('div.row.mb-4')

            div_table_data.remove()

        }
        else if(response.action ==='quantity-upadate'){
            console.log(response)
            if(response.orderitem_quantity === 0){
                var div_table_data = mythis.parents('div.row.mb-4')

                div_table_data.remove()
            }
            if ( response.orderitem_count==0 ) {
       
                $("#checkout-btn").addClass("disabled");
             }

            mythis.parents('div.item-price-quantity').find(".item-price").html(response.orderitem_price)
            mythis.parents('div.item-price-quantity').find("#item-quantity").html(response.orderitem_quantity)

            cart_count_divs = document.getElementsByClassName( 'cart-item-num' );

            [].slice.call( cart_count_divs  ).forEach(function ( cart_count_div  ) {
                cart_count_div.innerHTML = response.orderitem_count;
            });
            



            order_total_divs = document.getElementsByClassName( 'order-total' );

            [].slice.call( order_total_divs ).forEach(function ( order_total_div ) {
                order_total_div.innerHTML = response.order_total;
            });
          

        }
        
     }).fail((response)=>{
         alert(response)
     })
}




$('.update-cart').click( 
    function(){

    var productId = this.dataset.product
    var action = this.dataset.action
    var url = "/update-cart";
    console.log(url)
    cart_backend_request(url,productId,action,'')

});

//
$('.update-cart-list').click(function(){

    var action = this.dataset.action
    var productId = this.dataset.product
    
    var url = "/update-cart";

    cart_backend_request(url,productId,action,$(this))
    

    
    
})


//
$('.update-item-quantity').click(function(){

    var action = this.dataset.action
    var productId = this.dataset.product

    var url = "/update-cart";

    cart_backend_request(url,productId,action,$(this))

    console.log()
   

    
    
})