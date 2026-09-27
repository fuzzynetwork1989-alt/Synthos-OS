import { cn } from '../utils/cn'

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'outlined'
}

export function Card({ variant = 'default', className, children, ...props }: CardProps) {
  const baseStyles = 'rounded-lg'
  
  const variants = {
    default: 'bg-gray-900 border border-gray-800',
    elevated: 'bg-gray-900 border border-gray-800 shadow-lg',
    outlined: 'bg-transparent border border-gray-700',
  }
  
  return (
    <div className={cn(baseStyles, variants[variant], className)} {...props}>
      {children}
    </div>
  )
}

export function CardHeader({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn('p-6 border-b border-gray-800', className)} {...props}>
      {children}
    </div>
  )
}

export function CardContent({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn('p-6', className)} {...props}>
      {children}
    </div>
  )
}

export function CardFooter({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn('p-6 border-t border-gray-800', className)} {...props}>
      {children}
    </div>
  )
}
