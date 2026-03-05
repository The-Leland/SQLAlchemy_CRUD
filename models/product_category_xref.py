from db import db

products_categories_association_table = db.Table(
    "products_categories_association",   
    db.Model.metadata,
    db.Column(
        'product_id',
        db.ForeignKey('products.product_id', ondelete="CASCADE"),   
        primary_key=True
    ),
    db.Column(
        'category_id',
        db.ForeignKey('categories.category_id', ondelete="CASCADE"),  
        primary_key=True
    )
)