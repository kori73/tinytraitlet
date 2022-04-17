# tinytraitlet

tinytraitlet is a simple library that enables attribute validation and type checking for ``Traitful`` classes, inspired by traitlets library.

**Usage**

```python
from tinytraitlet import Traitful, String, validate, TraitError


class User(Traitful):
    name = String()
   
    @validate('name')
    def validate_name(self, value):
        if value == 'undefined':
            raise TraitError("Name cannot be 'undefined'")


class SubscriptionUser(User):
    subscription = String()
   
    @validate('subscription')
    def validate_subscription(self, value):
        if value not in ["monthly", "yearly"]:
            raise TraitError("subscription must be either 'monthly' or 'yearly'")
```

These classes behave as one would expect. ``@validate('name')`` decorator registers the ``validate_name`` method as the validator for the ``name`` trait. ``SubscriptionUser`` inherits both the ``name`` trait and the ``validate_name`` validator.

```python
>>> user = User(name="Niki")
>>> user.name
'Niki'
>>> user = SubscriptionUser(name="undefined")
tinytraitlet.TraitError: Name cannot be 'undefined'
>>> user = SubscriptionUser(subscription="yearly")
>>> user.subscription
'yearly'
>>> user.subscription = "daily"
tinytraitlet.TraitError: subscription must be either 'monthly' or 'yearly'
```

**Defining custom types:**
We should define ``default_value`` and ``model_type`` attributes. Example:
```python
from tinytraitlet import Model

class Integer(Model):
    default_value = 0
    model_type = int
```
**Why solve the same problem?**

tinytraitlet does not use metaclasses unlike traitlets. This reduces the chance of metaclass conflict. tinytraitlet is a simple alternative, currently under 100 lines of code, and offers only the absolutely essential functionality.


**Limitations**
- Currently a single trait type is defined: ``String``.
- Default values are not validated.
- Cross validation is not supported.
- A trait cannot have multiple validators
