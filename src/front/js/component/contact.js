import React, { useState, useContext } from 'react'
import { Context } from '../store/appContext'
import { useNavigate } from "react-router-dom";

export const Contact = (props) => {
    const {store, actions} = useContext(Context);
    const nagivate = useNavigate();
    const contact = props.contact;
    

    const imageUrl = 'https://cdn.icon-icons.com/icons2/1509/PNG/512/contactnew_104150.png'

    const nagivateEdit = () => {
        nagivate(`/contacts/${contact.id}`)
    }

    return(
        <div className='row border border-dark rounded m-3 py-1'>
            <div className='col-md-2 d-flex justify-content-center align-items-center'>
                <div className='d-none d-sm-none d-md-blocfa-6x iconk'>
                    <i className="fa-solid fa-address-book "></i>
                    {/* <img className='img-fluid' src={imageUrl} alt='contact photo'></img> */}
                </div>
            </div>
            <div className='col-md-8'>
                <div className='m-1'><i className="fa-solid fa-user me-2 icon"></i>Name: {contact.name}</div>
                <div className='m-1'><i className="fa-solid fa-phone me-2 icon"></i>Phone: {contact.phone}</div>
                <div className='m-1'><i className="fa-solid fa-envelope me-2 icon"></i>Email: {contact.email}</div>
                <div className='m-1'><i className="fa-solid fa-location-dot me-2 icon"></i>Address: {contact.address}</div>
            </div>
            <div className='col-md-2 d-flex justify-content-center'>
                {loggedIn ? 
                <button className='btn' onClick={nagivateEdit}>
                    <i className="fa-solid fa-pencil icon"></i>
                </button> :
                <button className='btn' disabled>
                    <i className="fa-solid fa-pencil icon"></i>
                </button>}
                <button className='btn' data-bs-target={`#modal${contact.id}`} data-bs-toggle="modal">
                    <i className="fa-solid fa-trash icon"></i>
                </button>
            </div>
        </div>

    )
}
