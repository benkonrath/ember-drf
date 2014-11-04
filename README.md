# Overview

This project aims to create a python package that makes it simple to build an
API that is compatible with
[Ember Data](https://github.com/emberjs/data)
out of the box. While initially the user will still be required to configure
their urls and serializers in a certain way for them to work properly, the
goal is to make this as pluggable as possible.

# Installation

TODO

# How to Use

The following is a complete list of steps to configure your api to work with
Ember-Data out of the box.

1. Serializers

You must expose only subclasses of `SideloadSerializer` from your viewsets in
order for them to work properly with Ember-Data.

```python
# serializers.py
from rest_framework.serializers import ModelSerializer
from drf_ember.serializers import SideloadSerializer
from my_app.models import Fruit

class FruitSerializer(ModelSerializer):
    class Meta:
        model = Fruit
        fields = ('basket', 'tree')

class FruitSideloadSerializer(SideloadSerializer):
    class Meta:
        base_serializer = FruitSerializer
        sideloads = [
            (Basket, BasketSerializer)
        ]
```

```python
# viewsets.py
class FruitViewset(ModelViewSet):
    model = Fruit
    serializer_class = FruitSideloadSerializer
```

Assuming that basket and tree are both one-to-many relationships, the
Ember-Data model could look like this:

```javascript
export default DS.Model.extend({
    basket: DS.belongsTo('basket'),
    tree: DS.belongsTo('tree', {async: true}) // async because no sideloads
});
```

SideloadSerializer also supports Embedded Records using the standard
`rest_framework` syntax.  Information on using EmbeddedRecords in Ember can
be found [here](http://emberjs.com/api/data/classes/DS.EmbeddedRecordsMixin.html).

2. Renders/Parsers

Ember-Data offers two built-in serializers, `DS.EmberJSONSerializer` and
`DS.ActiveRecordJSONSerializer`.  `DS.EmberJSONSerializers` is enabled by
default.  However, you may want to use ActiveRecordJSONSerializer as it
conforms more closely to the standard DRF output (e.g. underscored urls and
properties).  Either way you will need to configure DRF to use the
renderers and parsers provided by `drf_ember`.

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        # Choose one:
        'drf_ember.renderers.ActiveModelJSONRenderer',
        'drf_ember.renderers.EmberJSONRenderer',

        # leave this
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        # Choose one:
        'drf_ember.parsers.ActiveModelJSONParser',
        'drf_ember.parsers.EmberJSONRenderer',

        # leave this
        'rest_framework.parsers.MultiPartParser',
    ),
    # ... include other REST_FRAMEWORK settings as needed
}


Additional details on how to use renders can be found
[here](http://www.django-rest-framework.org/api-guide/renderers)

3. Urls

Ember will not by default append a trailing slash to urls.  [You can turn off
trailing slashes in django](https://docs.djangoproject.com/en/dev/ref/settings/#append-slash).  It is probably less intrusive to
make this change on the Ember side however:

```javascript
# adapters/application.js
import DS from "ember-data";
// alternatively, use DS.Adapter if you do not want to use ActiveModel
export default DS.ActiveModelAdapter.extend({
    buildURL: function(type, id, record){
        return this._super(type, id, record) + '/';
    }
});
```

4. CSRF

This is really outside of the scope of this project; however, in most cases
you will need to configure the Ember adapter to include a CSRF Token.  The
CSRF_TOKEN_VARIABLE is probably most easily set by embedding the csrf
token into the index.html template.

```javascript
# adapters/application.js
import DS from "ember-data";
// alternatively, use DS.Adapter if you do not want to use ActiveModel
export default DS.ActiveModelAdapter.extend({
    headers: {
        'X-CSRFToken': CSRF_TOKEN_VARIABLE
    }
});
```

5. Coalescing Find Requests

Ember-Data has a feature where it can [coalesce multiple single find requets
into a single query](http://emberjs.com/blog/2014/08/18/ember-data-1-0-beta-9-released.html).  To support this you will need to add `drf_ember.filters.CoallesceIDsFilterBackend`
to your FILTER_BACKENDS settings.

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'drf_ember.filters.CoallesceIDsFilterBackend'
    )
    # ... include other REST_FRAMEWORK settings as needed
}
