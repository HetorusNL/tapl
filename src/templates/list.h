// declare the 'single element' of the list
typedef struct list_TYPE_element_struct list_TYPE_element;
struct list_TYPE_element_struct {
    TYPE value;
    list_TYPE_element* next;
};
// declare the list type itself
typedef struct list_TYPE_struct list_TYPE;
struct list_TYPE_struct {
    list_TYPE_element* list;
};
// TODO: constructor and destructor
// get the size of a list
u64 list_TYPE_size(list_TYPE* this) {
    u64 size = 0;
    // simple case if the list is empty
    if (this->list == NULL)
        return 0;
    // otherwise traverse the list till we got the size
    list_TYPE_element* element = this->list;
    while (element != NULL) {
        size++;
        element = element->next;
    }
    return size;
}
// add an element to the back of the list
void list_TYPE_add(list_TYPE* this, TYPE value) {
    // construct the new element
    list_TYPE_element* new_element = malloc(sizeof(list_TYPE_element));
    new_element->value = value;
    new_element->next = NULL;

    // handle the empty list case
    if (this->list == NULL) {
        this->list = new_element;
        return;
    }

    // otherwise traverse to the end of the list
    list_TYPE_element* element = this->list;
    while (element->next != NULL)
        element = element->next;
    //  end found, add the new element
    element->next = new_element;
}
// gets the Xth element from the list, return 0/crash when it's not there
TYPE list_TYPE_get(list_TYPE* this, u64 index) {
    // traverse to the Xth element (if it exists)
    list_TYPE_element* element = this->list;
    while (element != NULL && index > 0) {
        element = element->next;
        index--;
    }

    // if the item is not found, or the element is NULL, return 0
    // TODO: or should we crash?
    if (index > 0 || element == NULL)
        return 0;

    // otherwise we have found the element, return the value
    return element->value;
}
// deletes the Xth element from the list, neatly reconnecting the respective pointer(s)
// return true on success, false/crash when it's not there
bool list_TYPE_del(list_TYPE* this, u64 index) {
    // handle the case when it's the first element
    if (index == 0) {
        // check if it exists
        if (this->list == NULL)
            return false;

        // otherise delete the element and connect the list to the inner element
        list_TYPE_element* inner = this->list->next;
        free(this->list);
        this->list = inner;
        return true;
    }
    // traverse to the X-1th element (if it exists)
    list_TYPE_element* element = this->list;
    while (element != NULL && index > 1) {
        element = element->next;
        index--;
    }

    // if the item is not found, or the element is NULL, return false
    // TODO: or should we crash?
    if (index > 1 || element == NULL || element->next == NULL)
        return false;

    // otherwise delete the next element and connect the element's next pointer to the next-next element
    list_TYPE_element* inner = element->next->next;
    free(element->next);
    element->next = inner;
}
// inserts a value at the Xth position in the list, neatly connecting the respective pointer(s)
// returns true on success, false/crash when it's not possible
bool list_TYPE_insert(list_TYPE* this, u64 index, TYPE value) {
    // handle the case when it's the first element
    if (index == 0) {
        // add the element to the list and move the current list value to the next pointer
        list_TYPE_element* new_element = malloc(sizeof(list_TYPE_element));
        new_element->value = value;
        new_element->next = this->list;
        this->list = new_element;
        return true;
    }

    // traverse to the Xth element (if it exists)
    list_TYPE_element* element = this->list;
    while (element != NULL && index > 0) {
        element = element->next;
        index--;
    }

    // if the item is not found, or the element is NULL, return false
    // TODO: or should we crash?
    if (index > 0 || element == NULL)
        return false;

    // add the element at the current element's next pointer, and this next pointer points to that
    list_TYPE_element* new_element = malloc(sizeof(list_TYPE_element));
    new_element->value = value;
    new_element->next = element->next;
    element->next = new_element;
    return true;
}
