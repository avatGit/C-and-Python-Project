#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_PRODUCTS 100
#define NAME_SIZE 50

typedef struct {
    int id;
    char name[NAME_SIZE];
    int quantity;
} Product;

Product inventory[MAX_PRODUCTS];
int productCount = 0;

void saveInventory() {
    FILE *file = fopen("stock.txt", "w");
    if (file == NULL) {
        printf("Error opening file.\n");
        return;
    }
    for (int i = 0; i < productCount; i++) {
        fprintf(file, "%d %s %d\n", inventory[i].id, inventory[i].name, inventory[i].quantity);
    }
    fclose(file);
}

void addProduct() {
    if (productCount >= MAX_PRODUCTS) {
        printf("Inventory full.\n");
        return;
    }
    Product p;
    printf("Product ID: ");
    scanf("%d", &p.id);
    printf("Product name: ");
    scanf("%s", p.name);
    printf("Quantity: ");
    scanf("%d", &p.quantity);
    inventory[productCount++] = p;
    printf("Product added.\n");
}

void displayProducts() {
    printf("\nProduct list:\n");
    for (int i = 0; i < productCount; i++) {
        printf("ID: %d | Name: %s | Quantity: %d\n", inventory[i].id, inventory[i].name, inventory[i].quantity);
    }
}

void modifyProduct() {
    int id;
    printf("ID of product to modify: ");
    scanf("%d", &id);
    for (int i = 0; i < productCount; i++) {
        if (inventory[i].id == id) {
            printf("New name: ");
            scanf("%s", inventory[i].name);
            printf("New quantity: ");
            scanf("%d", &inventory[i].quantity);
            printf("Product modified.\n");
            return;
        }
    }
    printf("Product not found.\n");
}

void deleteProduct() {
    int id;
    printf("ID of product to delete: ");
    scanf("%d", &id);
    for (int i = 0; i < productCount; i++) {
        if (inventory[i].id == id) {
            for (int j = i; j < productCount - 1; j++) {
                inventory[j] = inventory[j + 1];
            }
            productCount--;
            printf("Product deleted.\n");
            return;
        }
    }
    printf("Product not found.\n");
}

void searchProduct() {
    char search[NAME_SIZE];
    printf("Enter product name or ID: ");
    scanf("%s", search);
    int searchId = atoi(search);
    for (int i = 0; i < productCount; i++) {
        if (inventory[i].id == searchId || strcmp(inventory[i].name, search) == 0) {
            printf("Product found - ID: %d | Name: %s | Quantity: %d\n", inventory[i].id, inventory[i].name, inventory[i].quantity);
            return;
        }
    }
    printf("Product not found.\n");
}

int main() {
    int choice;
    do {
        printf("\n--- Product Management ---\n");
        printf("1. Add a product\n");
        printf("2. Modify a product\n");
        printf("3. Delete a product\n");
        printf("4. Display products\n");
        printf("5. Search for a product\n");
        printf("6. Save data\n");
        printf("0. Exit\n");
        printf("Your choice: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1: addProduct(); break;
            case 2: modifyProduct(); break;
            case 3: deleteProduct(); break;
            case 4: displayProducts(); break;
            case 5: searchProduct(); break;
            case 6: saveInventory(); break;
            case 0: printf("Goodbye.\n"); break;
            default: printf("Invalid choice.\n");
        }
    } while (choice != 0);
    return 0;
}