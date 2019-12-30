from .utils import FormValidator, BulkManager
from .models import Blog, BlogTag, Author


class CreateBlogForm(FormValidator):
    
    def validate_author_id(self):
        author_id = self.data.get("author_id", None)
        if not author_id:
            return self.errors.update({"author_id":"The author_id feild is required."})

        if not Author.objects.filter(id=author_id).exists():
            return self.errors.update({"author_id":"Author {author_id} does not exist".format(author_id=author_id)})
        
        self.cleaned_data["author_id"] = author_id         

    def validate_title(self):
        title = self.data.get("title", None)
        if not title:
            return self.errors.update({"title":"The title feild is required."})
        if len(title) < 10:
            return self.errors.update({"title":"Title is too short."})
        
        self.cleaned_data["title"] = title 


    def save(self):
        data = self.data
        data.update(self.cleaned_data)

        blog = Blog()
        for key, val in data.items():
            setattr(blog, key, val)
        blog.save()

        BulkManager(
            BlogTag,
            data.tags,
            update_dict={"blog_id": blog.id},
            removed_items=data.deleted_tags,
        )
        return blog