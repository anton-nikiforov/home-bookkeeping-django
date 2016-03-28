$(document).ready(function() 
{
	var _c = function(a) {return $(document.createElement(a));}
	
	window.HashtagsList = function(config)
	{
		$this = $(config.wrapper);

		this.wrapper	= config.wrapper;
		this.search_url	= $this.data('search-url');
		this.create_url = $this.data('create-url');

		this.hashtags 	= [];
		this.choosen	= [];
		
		this.findTag 	= $('input[data-action="findTag"]', this.wrapper);
		this.btnAdd 	= $('[data-action="addTag"]', this.wrapper);
		this.hidden		= $('.form-group__tags', this.wrapper);
		this.list		= $('.form-group__list', this.wrapper);
		this.result		= $('.form-group__result', this.wrapper);
	};
	
	HashtagsList.prototype.init = function()
	{
		var _this = this;
	
		$(_this.findTag).on('keyup', function(event)
		{
			var tag = _this.findTag.val();
			_this.result.empty();
			_this.list.empty();
			_this.hashtags = [];
		
			if(!tag.length) {
				return false;
			}
		
			$.post(_this.search_url, {
				'tag': tag,
				'choosen': _this.choosen
			}, function(data)
			{
				if(data.action) {
					_this.result.text('Found: ' + Object.keys(data.hashtags).length);

					_this.hashtags = data.hashtags;
					_this.buildList(data.hashtags);
				}
				else {
					_this.result.text(data.message);
				}
			}, 'json');
			
			delete tag;
		});
		
		$(_this.btnAdd).on('click', function(event)
		{
			if(confirm("Do you want to add hashtag '" + _this.findTag.val() + "'?") == true)
			{
				$.post(_this.create_url, {
					'tag': _this.findTag.val()
				}, function(data) 
				{
					if(!!data.action) {
						$.extend(_this.hashtags, data.info);
						_this.choose(data.ID);
					} 
					else {
						alert(data.message);
					}
				}, 'json');				
			}
		});
	};
	
	HashtagsList.prototype.buildList = function(items)
	{	
		console.log(items);
		for (var i in items) 
		{
			this.list.append(
				_c('div')
					.attr('data-id', items[i]['id'])
					.append([
						_c('input')
							.attr({'type': 'checkbox', 'id': 'input_' + items[i]['id']})
							.on('change', this.toggleChoose.bind(this, items[i]['id'])),
						_c('label')
							.attr('for', 'input_' + items[i]['id'])
							.text(items[i]['title'])
					])
			);
		}
	};
	
	HashtagsList.prototype.toggleChoose = function(ID)
	{
		$('#input_' + ID).is(':checked') ? this.choose(ID) : this.unchoose(ID);
	};
	
	HashtagsList.prototype.choose = function(ID)
	{
		if(this.choosen.indexOf(ID) == -1)
		{
			this.choosen.push(ID);
			
			this.hidden.append(
				_c('span').addClass("label label-primary hashtag_" + ID).data('hashtag', ID).text(this.hashtags[ID]['title']).append([
					_c('a').attr('href', 'javascript:void(0);').addClass('glyphicon glyphicon-remove').on('click', this.unchoose.bind(this, ID)),
					_c('input').attr({
						'type': 'hidden',
						'value': ID,
						'name': 'hashtags'
					})
				])
			);
		}
	};
	
	HashtagsList.prototype.unchoose = function(ID)
	{
		delete this.choosen[this.choosen.indexOf(ID)];
		this.hidden.find('.hashtag_'+ ID).remove();
		
		var i = $('#input_' + ID), c = i.length ? i.attr('checked', false) : null;
	};
	
	HashtagsList.prototype.addChoose = function(hashtag)
	{	
		var info = new Array();
		info[hashtag['id']] = hashtag;
	
		$.extend(this.hashtags, info);
		this.choose(hashtag['id']);
	};

	$('.hashtags_widget').each(function() {
		var hashtag = new HashtagsList({
			'wrapper': this
		});
		hashtag.init();

		$(hashtag.hidden).find('[data-hashtag]').each(function() {
			hashtag.choosen.push($(this).data('hashtag'));
		});
	});
});
