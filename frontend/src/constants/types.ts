export interface registerUserProps {
    name: string;
    email: string;
    password: string;
    password_confirmation: string;
    phone_number: string;
};

export interface loginUserProps {
    email: string;
    password: string;
};