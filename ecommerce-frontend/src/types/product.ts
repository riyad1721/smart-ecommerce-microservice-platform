export type Product = {
  id: string | number;
  name: string;
  description?: string;
  price: number;
  stock?: number;
  category_id?: string | number;
  category?: string;
  image_url?: string;
};

export type Category = {
  id: string | number;
  name: string;
};

export type ProductPayload = {
  name: string;
  description?: string;
  price: number;
  stock: number;
  category_id: number;
};
