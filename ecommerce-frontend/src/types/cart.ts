import type { Product } from './product';

export type CartItem = {
  id: string;
  item_id?: string;
  product_id: string;
  product?: Product;
  product_name?: string;
  quantity: number;
  price?: number;
  total_price?: number;
};

export type Cart = {
  id?: string;
  user_id?: string;
  items: CartItem[];
  total?: number;
  total_amount?: number;
};
