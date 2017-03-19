$(function() {
	// Updater
	$('.b-rent__submit').on('click', function() {
		$this = $(this);

		$this.prop('disabled', true);
		widget = '.m-product__' + $this.data('product');




		var rent_url = '/catalog/api/json/rent/add/';
		var csrfmiddlewaretoken = $this.data('csrf')
		var rent_data = {
			'product': $this.data('product'),
			'csrfmiddlewaretoken': csrfmiddlewaretoken,
			'rent_from': $(widget + ' .m-field__rent_from .b-field__field').val(),
			'rent_to': $(widget + ' .m-field__rent_to .b-field__field').val(),
			'rent_count': $(widget + ' .m-field__rent_count .b-field__field').val()
		};


		$(widget + ' .b-field__error').text('');


		$.post(rent_url, rent_data).done(function(rent_response) {
			var bucket_url = '/bucket/update/';

			var bucket_data = {
				'csrfmiddlewaretoken': csrfmiddlewaretoken,
				'content_type': rent_response['content_type'],
				'object_id': rent_response['object_id'],
				'count': $(widget + ' .m-field__rent_count .b-field__field').val()
			};

			console.log(bucket_data);

			if (rent_response.status == true) {
				$.post(bucket_url, bucket_data).done(function(bucket_response) {
					if (bucket_response.status == 'ok') {
						console.log(bucket_response);

						$('.b-button_extra').show();
						$('.b-button_bucket').show();
						$('.b-product__rent').hide();

						$this.prop('disabled', false);
					}
				}).fail(function(bucket_response) {
					alert('ajax error: bucket add');
				});
			} else {
				for (var key in rent_response.errors) {
					let value = rent_response.errors[key][0];
					$(widget + ' .m-field__' + key + ' .b-field__error').text(value);
					$this.prop('disabled', false);
				}
			}
 		}).fail(function(rent_response) {
			alert('ajax error: rend add');
		});


	});

	$('.b-button_extra').on('click', function(e) {
		$('.b-button_extra').hide();
		$('.b-product__rent').show();
	});
});