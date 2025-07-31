# 📊 **SAMPLE DATA QUERIES - TEXT OUTPUT**

## **Database: ecommerce_improved.db**
**Total Records: 29,120 products**

---

## **1️⃣ BASIC STATISTICS**
```
📦 Total Products: 29,120
🏷️  Unique Categories: 26
🏪 Unique Brands: 2,757
```

## **2️⃣ DEPARTMENT DISTRIBUTION**
```
department  count  percentage
     Women  15989       54.91
       Men  13131       45.09
```

## **3️⃣ PRICE ANALYSIS**
```
💰 Price Statistics:
   Minimum: $0.02
   Maximum: $999.00
   Average: $59.22
```

## **4️⃣ TOP 10 BRANDS BY PRODUCT COUNT**
```
         brand  product_count
     Allegra K           1034
  Calvin Klein            497
      Carhartt            388
         Hanes            308
        Volcom            292
       Nautica            263
        Levi's            259
    Quiksilver            257
Tommy Hilfiger            251
      Columbia            236
```

## **5️⃣ TOP 10 CATEGORIES**
```
                     category  product_count
                    Intimates           2363
                        Jeans           1999
                  Tops & Tees           1868
Fashion Hoodies & Sweatshirts           1866
                         Swim           1798
               Sleep & Lounge           1771
                       Shorts           1765
                     Sweaters           1737
                  Accessories           1559
                       Active           1432
```

## **6️⃣ SAMPLE PRODUCTS BY DEPARTMENT**

### **👔 MEN'S PRODUCTS:**
```
ID: 21046, Name: Wrangler Men's Genuine Loose Fit Jean..., Brand: Wrangler, Price: $40.00
ID: 24518, Name: Wigwam Men's Hiking/Outdoor Pro Length Sock..., Brand: Wigwam, Price: $15.44
ID: 24939, Name: American Apparel Solid Knee-High Sock..., Brand: American Apparel, Price: $10.00
```

### **👗 WOMEN'S PRODUCTS:**
```
ID: 1078, Name: Queenshiny Long Women's Knitted Rex Rabbit Fur Vest..., Brand: Queenshiny, Price: $189.00
ID: 7273, Name: Alfred Dunner Classics Elastic Waist Straight Skirt..., Brand: Alfred Dunner, Price: $22.99
ID: 7585, Name: Sutton Studio Single Button Jacket Vanilla..., Brand: Sutton Studio, Price: $44.78
```

## **7️⃣ PRICE RANGE ANALYSIS**
```
price_range  product_count
  Under $10           1345
    $10-$25           6494
    $25-$50          10074
   $50-$100           7148
  Over $100           4059
```

## **8️⃣ DATA QUALITY CHECK**
```
                     check_type  count
                 Total Products  29120
     Products with valid prices  29120
Products with valid departments  29120
 Products with valid SKU length  29120
```

---

## **✅ KEY INSIGHTS:**

1. **Data Quality**: 100% of products pass all validation checks
2. **Department Split**: Women's products (54.91%) slightly outnumber Men's (45.09%)
3. **Price Distribution**: Most products fall in the $25-$50 range (10,074 products)
4. **Top Brand**: Allegra K leads with 1,034 products
5. **Top Category**: Intimates is the largest category with 2,363 products
6. **Price Range**: From $0.02 to $999.00 with an average of $59.22

**Status**: ✅ **All queries executed successfully!** 