<!--⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# Integrate any ML framework with the Hub

The Hugging Face Hub makes hosting and sharing models with the community easy. It supports
[dozens of libraries](https://huggingface.co/docs/hub/models-libraries) in the Open Source ecosystem. We are always
working on expanding this support to push collaborative Machine Learning forward. The `huggingface_hub` library plays a
key role in this process, allowing any Python script to easily push and load files.

There are four main ways to integrate a library with the Hub:
1. **Push to Hub:** implement a method to upload a model to the Hub. This includes the model weights, as well as
   [the model card](https://huggingface.co/docs/huggingface_hub/how-to-model-cards) and any other relevant information
   or data necessary to run the model (for example, training logs). This method is often called `push_to_hub()`.
2. **Download from Hub:** implement a method to load a model from the Hub. The method should download the model
   configuration/weights and load the model. This method is often called `from_pretrained` or `load_from_hub()`.
3. **Inference API:** use our servers to run inference on models supported by your library for free.
4. **Widgets:** display a widget on the landing page of your models on the Hub. It allows users to quickly try a model
   from the browser.

In this guide, we will focus on the first two topics. We will present the two main approaches you can use to integrate
a library, with their advantages and drawbacks. Everything is summarized at the end of the guide to help you choose
between the two. Please keep in mind that these are only guidelines that you are free to adapt to you requirements.

If you are interested in Inference and Widgets, you can follow [this guide](https://huggingface.co/docs/hub/models-adding-libraries#set-up-the-inference-api).
In both cases, you can reach out to us if you are integrating a library with the Hub and want to be listed
[in our docs](https://huggingface.co/docs/hub/models-libraries).

## A flexible approach: helpers

The first approach to integrate a library to the Hub is to actually implement the `push_to_hub` and `from_pretrained`
methods by yourself. This gives you full flexibility on which files you need to upload/download and how to handle inputs
specific to your framework. You can refer to the two [upload files](./upload) and [download files](./download) guides
to learn more about how to do that. This is, for example how the FastAI integration is implemented (see [`push_to_hub_fastai`]
and [`from_pretrained_fastai`]).

Implementation can differ between libraries, but the workflow is often similar.

### from_pretrained

This is how a `from_pretrained` method usually look like:

```python
def from_pretrained(model_id: str) -> MyModelClass:
   # Download model from Hub
   cached_model = hf_hub_download(
      repo_id=repo_id,
      filename="model.pkl",
      library_name="fastai",
      library_version=get_fastai_version(),
   )

   # Load model
    return load_model(cached_model)
```

### push_to_hub

The `push_to_hub` method often requires a bit more complexity to handle repo creation, generate the model card and save weights.
A common approach is to save all of these files in a temporary folder, upload it and then delete it.

```python
def push_to_hub(model: MyModelClass, repo_name: str) -> None:
   api = HfApi()

   # Create repo if not existing yet and get the associated repo_id
   repo_id = api.create_repo(repo_name, exist_ok=True)

   # Save all files in a temporary directory and push them in a single commit
   with TemporaryDirectory() as tmpdir:
      tmpdir = Path(tmpdir)

      # Save weights
      save_model(model, tmpdir / "model.safetensors")

      # Generate model card
      card = generate_model_card(model)
      (tmpdir / "README.md").write_text(card)

      # Save logs
      # Save figures
      # Save evaluation metrics
      # ...

      # Push to hub
      return api.upload_folder(repo_id=repo_id, folder_path=tmpdir)
```

This is of course only an example. If you are interested in more complex manipulations (delete remote files, upload
weights on the fly, persist weights locally, etc.) please refer to the [upload files](./upload) guide.

### Limitations

While being flexible, this approach has some drawbacks, especially in terms of maintenance. Hugging Face users are often
used to additional features when working with `huggingface_hub`. For example, when loading files from the Hub, it is
common to offer parameters like:
- `token`: to download from a private repo
- `revision`: to download from a specific branch
- `cache_dir`: to cache files in a specific directory
- `force_download`/`resume_download`/`local_files_only`: to reuse the cache or not
- `proxies`: configure HTTP session

When pushing models, similar parameters are supported:
- `commit_message`: custom commit message
- `private`: create a private repo if missing
- `create_pr`: create a PR instead of pushing to `main`
- `branch`: push to a branch instead of the `main` branch
- `allow_patterns`/`ignore_patterns`: filter which files to upload
- `token`
- ...

All of these parameters can be added to the implementations we saw above and passed to the `huggingface_hub` methods.
However, if a parameter changes or a new feature is added, you will need to update your package. Supporting those
parameters also means more documentation to maintain on your side. To see how to mitigate these limitations, let's jump
to our next section **class inheritance**.

## A more complex approach: class inheritance

As we saw above, there are two main methods to include in your library to integrate it with the Hub: upload files
(`push_to_hub`) and download files (`from_pretrained`). You can implement those methods by yourself but it comes with
caveats. To tackle this, `huggingface_hub` provides a tool that uses class inheritance. Let's see how it works!

In a lot of cases, a library already implements its model using a Python class. The class contains the properties of
the model and methods to load, run, train, and evaluate it. Our approach is to extend this class to include upload and
download features using mixins. A [Mixin](https://stackoverflow.com/a/547714) is a class that is meant to extend an
existing class with a set of specific features using multiple inheritance. `huggingface_hub` provides its own mixin,
the [`ModelHubMixin`]. The key here is to understand its behavior and how to customize it.

The [`ModelHubMixin`] class implements 3 *public* methods (`push_to_hub`, `save_pretrained` and `from_pretrained`). Those
are the methods that your users will call to load/save models with your library. [`ModelHubMixin`] also defines 2
*private* methods (`_save_pretrained` and `_from_pretrained`). Those are the ones you must implement. So to integrate
your library, you should:

1. Make your Model class inherit from [`ModelHubMixin`].
2. Implement the private methods:
    - [`~ModelHubMixin._save_pretrained`]: method taking as input a path to a directory and saving the model to it.
    You must write all the logic to dump your model in this method: model card, model weights, configuration files,
    training logs, and figures. Any relevant information for this model must be handled by this method.
    [Model Cards](https://huggingface.co/docs/hub/model-cards) are particularly important to describe your model. Check
    out [our implementation guide](./model-cards) for more details.
    - [`~ModelHubMixin._from_pretrained`]: **class method** taking as input a `model_id` and returning an instantiated
    model. The method must download the relevant files and load them.
3. You are done!

The advantage of using [`ModelHubMixin`] is that once you take care of the serialization/loading of the files, you are ready to go. You don't need to worry about stuff like repo creation, commits, PRs, or revisions. All of this is handled by the mixin and is available to your users. The Mixin also ensures that public methods are well documented and type annotated.

As a bonus, [`ModelHubMixin`] handles the model configuration for you. If your `__init__` method expects a `config` input, it will be automatically saved in the repo when calling `save_pretrained` and reloaded correctly by `load_pretrained`. Moreover, if the `config` input parameter is annotated with dataclass type (e.g. `config: Optional[MyConfigClass] = None`), then the `config` value will be correctly deserialized for you. Finally, all jsonable values passed at initialization will be also stored in the config file. This means you don't necessarily have to expect a `config` input to benefit from it. The big advantage of having a `config.json` file in your model repository is that it automatically enables the analytics on the Hub (e.g. the "downloads" count).

Finally, [`ModelHubMixin`] handles generating a model card for you. When inheriting from [`ModelHubMixin`], you can define metadata such as `library_name`, `tags`, `repo_url` and `docs_url`. Those fields will be reused to populate the modelcard of any model that use your class. This is very practical to make all models using your library easily searchable on the Hub and to provide some resource links for users landing on the Hub. If you want to extend the modelcard template, you can override the [`~ModelHubMixin.generate_model_card`] method.

### A concrete example: PyTorch

A good example of what we saw above is [`PyTorchModelHubMixin`], our integration for the PyTorch framework. This is a ready-to-use integration.

#### How to use it?

Here is how any user can load/save a PyTorch model from/to the Hub:

```python
>>> import torch
>>> import torch.nn as nn
>>> from huggingface_hub import PyTorchModelHubMixin


# Define your Pytorch model exactly the same way you are used to
>>> class MyModel(
...         nn.Module,
...         PyTorchModelHubMixin, # multiple inheritance
...         library_name="keras-nlp",
...         tags=["keras"],
...         repo_url="https://github.com/keras-team/keras-nlp",
...         docs_url="https://keras.io/keras_nlp/",
...         # ^ optional metadata to generate model card
...     ):
...     def __init__(self, hidden_size: int = 512, vocab_size: int = 30000, output_size: int = 4):
...         super().__init__()
...         self.param = nn.Parameter(torch.rand(hidden_size, vocab_size))
...         self.linear = nn.Linear(output_size, vocab_size)

...     def forward(self, x):
...         return self.linear(x + self.param)

# 1. Create model
>>> model = MyModel(hidden_size=128)

# Config is automatically created based on input + default values
>>> model._hub_mixin_config
{"hidden_size": 128, "vocab_size": 30000, "output_size": 4}

# 2. (optional) Save model to local directory
>>> model.save_pretrained("path/to/my-awesome-model")

# 3. Push model weights to the Hub
>>> model.push_to_hub("my-awesome-model")

# 4. Initialize model from the Hub => config has been preserved
>>> model = MyModel.from_pretrained("username/my-awesome-model")
>>> model._hub_mixin_config
{"hidden_size": 128, "vocab_size": 30000, "output_size": 4}

# Model card has been correctly populated
>>> from huggingface_hub import ModelCard
>>> card = ModelCard.load("username/my-awesome-model")
>>> card.data.tags
["keras", "pytorch_model_hub_mixin", "model_hub_mixin"]
>>> card.data.library_name
"keras-nlp"
```

#### Implementation

The implementation is actually very straightforward, and the full implementation can be found [here](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/hub_mixin.py).

1. First, inherit your class from `ModelHubMixin`:

```python
from huggingface_hub import ModelHubMixin

class PyTorchModelHubMixin(ModelHubMixin):
   (...)
```

2. Implement the `_save_pretrained` method:

```py
from huggingface_hub import ModelHubMixin

class PyTorchModelHubMixin(ModelHubMixin):
   (...)

    def _save_pretrained(self, save_directory: Path) -> None:
        """Save weights from a Pytorch model to a local directory."""
        save_model_as_safetensor(self.module, str(save_directory / SAFETENSORS_SINGLE_FILE))

```

3. Implement the `_from_pretrained` method:

```python
class PyTorchModelHubMixin(ModelHubMixin):
   (...)

   @classmethod # Must be a classmethod!
   def _from_pretrained(
      cls,
      *,
      model_id: str,
      revision: str,
      cache_dir: str,
      force_download: bool,
      proxies: Optional[Dict],
      resume_download: bool,
      local_files_only: bool,
      token: Union[str, bool, None],
      map_location: str = "cpu", # additional argument
      strict: bool = False, # additional argument
      **model_kwargs,
   ):
      """Load Pytorch pretrained weights and return the loaded model."""
        model = cls(**model_kwargs)
        if os.path.isdir(model_id):
            print("Loading weights from local directory")
            model_file = os.path.join(model_id, SAFETENSORS_SINGLE_FILE)
            return cls._load_as_safetensor(model, model_file, map_location, strict)

         model_file = hf_hub_download(
            repo_id=model_id,
            filename=SAFETENSORS_SINGLE_FILE,
            revision=revision,
            cache_dir=cache_dir,
            force_download=force_download,
            proxies=proxies,
            resume_download=resume_download,
            token=token,
            local_files_only=local_files_only,
            )
         return cls._load_as_safetensor(model, model_file, map_location, strict)
```

And that's it! Your library now enables users to upload and download files to and from the Hub.

## Quick comparison

Let's quickly sum up the two approaches we saw with their advantages and drawbacks. The table below is only indicative.
Your framework might have some specificities that you need to address. This guide is only here to give guidelines and
ideas on how to handle integration. In any case, feel free to contact us if you have any questions!

<!-- Generated using https://www.tablesgenerator.com/markdown_tables -->
| Integration | Using helpers | Using [`ModelHubMixin`] |
|:---:|:---:|:---:|
| User experience | `model = load_from_hub(...)`<br>`push_to_hub(model, ...)` | `model = MyModel.from_pretrained(...)`<br>`model.push_to_hub(...)` |
| Flexibility | Very flexible.<br>You fully control the implementation. | Less flexible.<br>Your framework must have a model class. |
| Maintenance | More maintenance to add support for configuration, and new features. Might also require fixing issues reported by users. | Less maintenance as most of the interactions with the Hub are implemented in `huggingface_hub`. |
| Documentation / Type annotation | To be written manually. | Partially handled by `huggingface_hub`. |
| Download counter | To be handled manually. | Enabled by default if class has a `config` attribute. |
| Model card | To be handled manually | Generated by default with library_name, tags, etc. |
