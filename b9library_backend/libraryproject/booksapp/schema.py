import strawberry
from typing import List, Union
import strawberry_django
from strawberry_django.optimizer import DjangoOptimizerExtension
from .models import Book
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async  # For async function

# ------ Types and Erros classes ------------


@strawberry_django.type(Book, fields="__all__")
class BookType:
    pass


@strawberry.type
class BookNotFoundError:
    message: str


@strawberry.type
class AddBookError:
    message: str
    field_errors: list[str] = strawberry.field(default_factory=list)


@strawberry.type
class BookUpdateSuccess:
    book: BookType


@strawberry.type
class BookDeleteSuccess:
    id: int


@strawberry.type
class Status:
    code: int
    status: str

# ---------- Query and Mutation classes ----------


@strawberry.type
# Get queries
class Query:

    # Check if api url is working
    @strawberry.field
    def status(self) -> Status:
        return Status(code=200, status="OK")

    # Get all books
    books: List[BookType] = strawberry_django.field()

    # Get book by id
    @strawberry.field
    async def book(self, id: int) -> Union[BookType, BookNotFoundError]:
        try:
            book = await sync_to_async(Book.objects.get)(id=id)
            # return Book.objects.get(id=id)
            return book
        except Book.DoesNotExist:
            raise BookNotFoundError(message=f"Book with id {id} not found.")


@strawberry.type
class Mutation:
    @strawberry_django.mutation(handle_django_errors=True)
    async def add_new_book(self, title: str, author: str, description: str, publish_year: int, cover_image: str = None) -> BookType:
        try:
            book = Book(
                title=title,
                author=author,
                description=description,
                publish_year=publish_year,
                cover_image=cover_image
            )
            await sync_to_async(book.full_clean)()
            await sync_to_async(book.save)()
            
            return book
        
        except Exception as e:
            return AddBookError(message=str(e))

    @strawberry_django.mutation(handle_django_errors=True)
    async def update_book(self, id: int, title: str, author: str, description: str, publish_year: int, cover_image: str = None) -> BookType:
        try:
            book = Book.objects.get(id=id)
            if title:
                book.title = title

            if author:
                book.author = author

            if description:
                book.description = description

            if publish_year:
                book.publish_year = publish_year

            if cover_image:
                book.cover_image = cover_image

            await sync_to_async(book.full_clean)()
            await sync_to_async(book.save)()
            
            return BookUpdateSuccess(book=book)
        
        except ObjectDoesNotExist:
            return BookNotFoundError(message=f"Book with id {id} not found.")
        except Exception as e:
            return AddBookError(message=str(e))

    @strawberry_django.mutation(handle_django_errors=True)
    async def delete_book(self, id: int) -> BookType:
        try:
            book = await sync_to_async(Book.objects.get)(id=id)
            await sync_to_async(book.delete)()
            
            return book
        
        except Book.DoesNotExist:
            return BookNotFoundError(message=f"Book with id {id} not found.")


schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=[
                           DjangoOptimizerExtension])
