import React from 'react'

function Navbar() {
    return (
        <nav className="flex justify-between items-center px-8 py-4 mx-auto">
            <h1 className="text-2xl font-semibold font-poppins">
                B9Library
            </h1>
            <ul className="flex items-center gap-x-10 font-poppins">
                <li>
                    <a href="#" className="text-lg hover:text-blue-500">
                        Home
                    </a>
                </li>
                <li>
                    <a href="#" className="text-lg hover:text-blue-500">
                        About
                    </a>
                </li>
                <li>
                    <a href="#" className="text-lg hover:text-blue-500">
                        Contact
                    </a>
                </li>
            </ul>
        </nav>
    )
}

export default Navbar