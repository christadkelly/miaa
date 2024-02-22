import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import { Context } from "../store/appContext";

import { Contact } from "../component/contact";
import { DeleteModal } from "../component/deleteModal";

export const ContactList = () => {
    const { store, actions } = useContext(Context);

    useEffect(()=>{
        actions.fetchUserContacts()
    }, [])

    return(
        <>
        <div className="container">
            <div className="row">
                <Link to='/contacts/new'>
                    <button className="btn btn-success mt-1">
                        Add New Contact
                    </button>
                </Link>
            </div>
            {store.userContacts && store.userContacts.length > 0 && store.userContacts.map((contact, key) => {
                return <Contact key={key} contact={contact}/>
            })}
        </div>
        {/* <div className="modal-fade">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h1>Delete Contact</h1>
                        <button type="button" className="btn-close" aria-label="Close modal" onClick={actions.hideDeleteContact(false)}></button>
                    </div>
                    <div className="modal-body">
                        <h6 className="text-center"> 
                            Are you sure you would like to delete this contact? 
                            Once deleted, the contact cannot be recovered
                        </h6>
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-secondary"onClick={actions.hideDeleteContact(false)}>Close</button>
                        <button type="button" className="btn btn-danger">Delete Contact</button>
                    </div>
                </div>
            </div>
        </div> */}
        </>
    )
}
