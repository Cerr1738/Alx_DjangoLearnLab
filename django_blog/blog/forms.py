from django import forms
from .models import Post, Comment, Tag

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas",
        widget=forms.TextInput(attrs={"placeholder": "e.g. Django, Python, Web"})
    )

    class Meta:
        model = Post
        fields = ["title", "content", "tags"]

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            # process tags
            tags_str = self.cleaned_data.get("tags", "")
            if tags_str:
                tag_names = [t.strip() for t in tags_str.split(",") if t.strip()]
                tag_objs = []
                for name in tag_names:
                    tag_obj, created = Tag.objects.get_or_create(name=name)
                    tag_objs.append(tag_obj)
                post.tags.set(tag_objs)
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
