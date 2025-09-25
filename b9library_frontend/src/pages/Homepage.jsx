import React from 'react'
import books from "../data/DUMMY_DATA.json"
import BookCard from '../components/BookCard'

function Homepage() {
    return (
        <div className='w-full flex items-center flex-wrap gap-10 my-10 mx-auto'>
            {
                books.map((book) => {
                    return (
                        <BookCard key={book.title} book={book} />
                    )
                })
            }
        </div>
    )
}

export default Homepage