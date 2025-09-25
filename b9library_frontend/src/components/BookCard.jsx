import React from 'react'

function BookCard({ book }) {
    return (
        <div key={book.title} className='w-full max-w-[350px] h-[500px] flex flex-col items-center justify-center gap-2 px-5 py-7 shadow-md shadow-gray-400 text-center transition 
              duration-300 
              ease-in-out 
              hover:scale-105 cursor-pointer'>
            <div className='w-[80%] h-[70%]'>
                <img src={book.cover_image} alt={book.title} className='w-full h-full object-fill' />
            </div>
            <div className='w-full my-3 flex flex-col gap-3'>
                <p className='text-lg font-bold'>{book.title}</p>
                <p>{book.author}</p>
                <p>{book.publish_year}</p>
            </div>
        </div>
    )
}

export default BookCard