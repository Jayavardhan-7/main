import React, { createContext, useContext, useState, useEffect } from "react";
import { photographers as initialData } from "../data/photographers";

export interface Photographer {
    id: string;
    name: string;
    role: string;
    city: string;
    price: string;
    description: string;
    image: string;
    rating: number;
    reviews: number;
    portfolio: string[];
    specialty: string;
    whyChosen: string;
    mapQuery: string;
    status: 'approved' | 'pending' | 'rejected';
    email?: string;
    password?: string;
    instaUrl?: string;
}

export interface Booking {
    id: string;
    userId: string;
    photographerId: string;
    photographerName: string;
    photographerImage: string;
    photographerCity: string;
    date: string;
    totalAmount: number;
    status: string;
}

interface PhotographerContextType {
    photographers: Photographer[]; // Only approved
    allPhotographers: Photographer[]; // All (for admin)
    pendingPhotographers: Photographer[]; // Only pending
    bookings: Booking[];
    addPhotographer: (p: Photographer) => void;
    registerPhotographer: (p: Omit<Photographer, "id" | "status" | "rating" | "reviews">) => void;
    approvePhotographer: (id: string) => void;
    rejectPhotographer: (id: string) => void;
    updatePhotographer: (p: Photographer) => void;
    deletePhotographer: (id: string) => void;
    addBooking: (b: Booking) => void; // New helper method
    stats: {
        totalPhotographers: number;
        totalBookings: number;
        activeCities: number;
        pendingRequests: number;
    };
}

const PhotographerContext = createContext<PhotographerContextType | undefined>(undefined);

export const PhotographerProvider = ({ children }: { children: React.ReactNode }) => {
    const [photographersList, setPhotographersList] = useState<Photographer[]>([]);
    const [bookings, setBookings] = useState<Booking[]>([]);

    useEffect(() => {
        // Initialize Database Data
        fetch('/api/photographers/')
            .then(res => res.json())
            .then(data => {
                if (data.length === 0) {
                    const seeded = initialData.map(p => ({ ...p, status: 'approved' as 'approved' }));
                    fetch('/api/photographers/', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(seeded)
                    }).then(r => r.json()).then(setPhotographersList);
                } else {
                    setPhotographersList(data);
                }
            })
            .catch(console.error);

        fetch('/api/bookings/')
            .then(res => res.json())
            .then(setBookings)
            .catch(console.error);
    }, []);

    const addPhotographer = (p: Photographer) => {
        const newRecord = { ...p, status: p.status || 'approved' };
        fetch('/api/photographers/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newRecord)
        }).then(r => r.json()).then(saved => setPhotographersList(prev => [...prev, saved]));
    };

    const registerPhotographer = (data: Omit<Photographer, "id" | "status" | "rating" | "reviews">) => {
        const newRecord: Photographer = {
            ...data,
            id: Date.now().toString(),
            status: 'pending',
            rating: 0,
            reviews: 0
        };
        fetch('/api/photographers/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newRecord)
        }).then(r => r.json()).then(saved => setPhotographersList(prev => [...prev, saved]));
    };

    const approvePhotographer = (id: string) => {
        setPhotographersList(prev => prev.map(p => p.id === id ? { ...p, status: 'approved' as const } : p));
        fetch(`/api/photographers/${id}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: 'approved' })
        });
    };

    const rejectPhotographer = (id: string) => {
        setPhotographersList(prev => prev.filter(p => p.id !== id));
        fetch(`/api/photographers/${id}/`, { method: 'DELETE' });
    };

    const updatePhotographer = (updated: Photographer) => {
        setPhotographersList(prev => prev.map(p => p.id === updated.id ? updated : p));
        fetch(`/api/photographers/${updated.id}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updated)
        });
    };

    const deletePhotographer = (id: string) => {
        setPhotographersList(prev => prev.filter(p => p.id !== id));
        fetch(`/api/photographers/${id}/`, { method: 'DELETE' });
    };

    // New Booking Method targeting DB
    const addBooking = (b: Booking) => {
        fetch('/api/bookings/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(b)
        }).then(r => r.json()).then(saved => setBookings(prev => [...prev, saved]));
    };

    const approvedPhotographers = photographersList.filter(p => p.status === 'approved' || !p.status);
    const pendingPhotographers = photographersList.filter(p => p.status === 'pending');

    const stats = {
        totalPhotographers: approvedPhotographers.length,
        totalBookings: bookings.length,
        activeCities: new Set(approvedPhotographers.map(p => p.city)).size,
        pendingRequests: pendingPhotographers.length
    };

    return (
        <PhotographerContext.Provider value={{
            photographers: approvedPhotographers,
            allPhotographers: photographersList,
            pendingPhotographers,
            bookings,
            addPhotographer,
            registerPhotographer,
            approvePhotographer,
            rejectPhotographer,
            updatePhotographer,
            deletePhotographer,
            addBooking,
            stats
        }}>
            {children}
        </PhotographerContext.Provider>
    );
};

export const usePhotographers = () => {
    const context = useContext(PhotographerContext);
    if (!context) throw new Error("usePhotographers must be used within PhotographerProvider");
    return context;
};
