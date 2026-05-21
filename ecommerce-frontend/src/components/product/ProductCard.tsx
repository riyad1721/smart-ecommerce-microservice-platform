import { Edit3, ShoppingCart, Trash2 } from 'lucide-react';
import type { Product } from '../../types/product';
import { formatCurrency } from '../../utils/format';
import Button from '../common/Button';
import Card from '../common/Card';

type ProductCardProps = {
  product: Product;
  onAdd: (product: Product) => void;
  onEdit?: (product: Product) => void;
  onDelete?: (product: Product) => void;
  deleting?: boolean;
};

const ProductCard = ({ product, onAdd, onEdit, onDelete, deleting }: ProductCardProps) => (
  <Card className="flex h-full flex-col overflow-hidden p-0">
    <div className="flex h-36 shrink-0 items-center justify-center bg-gradient-to-br from-blue-50 to-slate-100 text-5xl">
      <ShoppingCart className="h-12 w-12 text-blue-500" />
    </div>

    <div className="flex flex-1 flex-col p-5">
      <div className="mb-2 flex items-start justify-between gap-3">
        <h3 className="text-lg font-bold text-slate-900">{product.name}</h3>
        <span className="shrink-0 rounded-full bg-blue-50 px-3 py-1 text-sm font-bold text-blue-700">
          {formatCurrency(product.price)}
        </span>
      </div>

      <p className="line-clamp-3 flex-1 text-sm text-slate-500">
        {product.description || 'No description available.'}
      </p>

      <div className="mt-4 flex items-center justify-between text-xs text-slate-500">
        <span>Stock: {product.stock ?? 'N/A'}</span>
        <span>{product.category || 'General'}</span>
      </div>

      <div className="mt-4 grid gap-2">
        <Button className="w-full" onClick={() => onAdd(product)}>
          <ShoppingCart className="h-4 w-4" /> Add to cart
        </Button>

        {(onEdit || onDelete) && (
          <div className="grid grid-cols-2 gap-2">
            {onEdit && (
              <Button variant="ghost" onClick={() => onEdit(product)}>
                <Edit3 className="h-4 w-4" /> Edit
              </Button>
            )}

            {onDelete && (
              <Button variant="danger" loading={deleting} onClick={() => onDelete(product)}>
                <Trash2 className="h-4 w-4" /> Delete
              </Button>
            )}
          </div>
        )}
      </div>
    </div>
  </Card>
);

export default ProductCard;
