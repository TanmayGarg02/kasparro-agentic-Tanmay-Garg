from core.models import Product, FictionalProduct


def extract_basic_info(product: Product):
    return {
        "name": product.product_name,
        "concentration": product.concentration,
        "skin_type": product.skin_type,
        "price": product.price
    }


def build_benefits_block(product: Product):
    return {
        "benefits_list": product.benefits,
        "benefits_summary": f"This product helps with {', '.join(product.benefits)}."
    }


def build_usage_block(product: Product):
    return {
        "how_to_use": product.how_to_use,
        "usage_summary": f"Use by following this method: {product.how_to_use}."
    }


def build_side_effects_block(product: Product):
    return {
        "side_effects": product.side_effects,
        "safety_note": f"Possible reactions include {product.side_effects}."
    }


def build_fictional_product_b():
    return FictionalProduct(
        product_name="RadiantPlus Brightening Serum",
        key_ingredients=["Niacinamide", "Aloe Vera"],
        benefits=["Brightening", "Oil control"],
        price=649
    )


def compare_products(product_a: Product, product_b: FictionalProduct):
    return {
        "product_a_name": product_a.product_name,
        "product_b_name": product_b.product_name,
        "ingredient_comparison": {
            "a_ingredients": product_a.key_ingredients,
            "b_ingredients": product_b.key_ingredients
        },
        "benefits_comparison": {
            "a_benefits": product_a.benefits,
            "b_benefits": product_b.benefits
        },
        "price_comparison": {
            "a_price": product_a.price,
            "b_price": product_b.price
        }
    }
