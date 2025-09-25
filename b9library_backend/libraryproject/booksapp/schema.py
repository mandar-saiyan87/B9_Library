import strawberry
from typing import List, Optional, Union
import strawberry_django
from strawberry_django.optimizer import DjangoOptimizerExtension
from .models import Book
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async  # For async function

# ------ Types and Erros classes ------------


@strawberry_django.type(Book, fields="__all__")
class BookType:
    pass


@strawberry.input
class UpdateBookInput:
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    publish_year: Optional[int] = None
    cover_image: Optional[str] = None


@strawberry.type
class BookNotFoundError:
    message: str


@strawberry.type
class AddBookError:
    message: str
    # To catch list of validation error in case (e.g. title is too long, author is required etc. Right now not much of validation is done)
    field_errors: list[str] = strawberry.field(default_factory=list)


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
    async def add_new_book(self, title: str, author: str, description: str, publish_year: int, cover_image: str = None) -> Union[BookType, AddBookError]:
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
    async def update_book(self, id: int, updateData: UpdateBookInput) -> Union[BookType, BookNotFoundError, AddBookError]:
        try:
            book = await sync_to_async(Book.objects.get)(id=id)

            if updateData.title is not None:
                book.title = updateData.title

            if updateData.author is not None:
                book.author = updateData.author

            if updateData.description is not None:
                book.description = updateData.description

            if updateData.publish_year:
                book.publish_year = updateData.publish_year

            if updateData.cover_image:
                book.cover_image = updateData.cover_image

            await sync_to_async(book.full_clean)()
            await sync_to_async(book.save)()

            return book

        except ObjectDoesNotExist:
            return BookNotFoundError(message=f"Book with id {id} not found.")
        except Exception as e:
            # Reusing AddBookError as it shares same validations
            return AddBookError(message=str(e))

    @strawberry_django.mutation(handle_django_errors=True)
    async def delete_book(self, id: int) -> Union[BookType, BookNotFoundError]:
        try:
            book = await sync_to_async(Book.objects.get)(id=id)
            await sync_to_async(book.delete)()

            return book

        except Book.DoesNotExist:
            return BookNotFoundError(message=f"Book with id {id} not found.")


schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=[
                           DjangoOptimizerExtension])
