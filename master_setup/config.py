# master_setup/config.py
from master_setup.views import (
    department_view,
    designation_view,
    shift_type_view,
    employee_type_view,
    account_type_view,
    tax_type_view,
    discount_type_view,
    payment_mode_view,
    currency_view,
    service_category_view,
    miscellaneous_service_view,
    event_type_view,
    parking_type_view,
    notification_category_view,
    notification_template_view,
    booking_source_view,
    country_view,
    printer_view,
)

from .datatables import (
    DepartmentDataTable,
    DesignationDataTable,
    ShiftTypeDataTable,
    EmployeeTypeDataTable,
    AccountTypeDataTable,
    TaxTypeDataTable,
    DiscountTypeDataTable,
    PaymentModeDataTable,
    CurrencyDataTable,
    ServiceCategoryDataTable,
    MiscellaneousServiceDataTable,
    EventTypeDataTable,
    ParkingTypeDataTable,
    NotificationCategoryDataTable,
    NotificationTemplateDataTable,
    BookingSourceDataTable,
    CountryDataTable,
    PrinterDataTable,
)

# Define all your CRUD entities in one place
MASTER_ENTITIES = [
    {
        'name': 'department',
        'view_module': department_view,
        'datatable_view': DepartmentDataTable,
        'verbose_name': 'Department'
    },
    {
        'name': 'designation',
        'view_module': designation_view,
        'datatable_view': DesignationDataTable,
        'verbose_name': 'Designation'
    },
    {
        'name': 'shift_type',
        'view_module': shift_type_view,
        'datatable_view': ShiftTypeDataTable,
        'verbose_name': 'Shift Type'
    },
    {
        'name': 'employee_type',
        'view_module': employee_type_view,
        'datatable_view': EmployeeTypeDataTable,
        'verbose_name': 'Employee Type'
    },
    {
        'name': 'account_type',
        'view_module': account_type_view,
        'datatable_view': AccountTypeDataTable,
        'verbose_name': 'Account Type'
    },
    {
        'name': 'tax_type',
        'view_module': tax_type_view,
        'datatable_view': TaxTypeDataTable,
        'verbose_name': 'Tax Type'
    },
    {
        'name': 'discount_type',
        'view_module': discount_type_view,
        'datatable_view': DiscountTypeDataTable,
        'verbose_name': 'Discount Type'
    },
    {
        'name': 'payment_mode',
        'view_module': payment_mode_view,
        'datatable_view': PaymentModeDataTable,
        'verbose_name': 'Payment Mode'
    },
    {
        'name': 'currency',
        'view_module': currency_view,
        'datatable_view': CurrencyDataTable,
        'verbose_name': 'Currency'
    },
    {
        'name': 'service_category',
        'view_module': service_category_view,
        'datatable_view': ServiceCategoryDataTable,
        'verbose_name': 'Service Category'
    },
    {
        'name': 'miscellaneous_service',
        'view_module': miscellaneous_service_view,
        'datatable_view': MiscellaneousServiceDataTable,
        'verbose_name': 'Miscellaneous Service'
    },
    {
        'name': 'event_type',
        'view_module': event_type_view,
        'datatable_view': EventTypeDataTable,
        'verbose_name': 'Event Type'
    },
    {
        'name': 'parking_type',
        'view_module': parking_type_view,
        'datatable_view': ParkingTypeDataTable,
        'verbose_name': 'Parking Type'
    },
    {
        'name': 'notification_category',
        'view_module': notification_category_view,
        'datatable_view': NotificationCategoryDataTable,
        'verbose_name': 'Notification Category'
    },
    {
        'name': 'notification_template',
        'view_module': notification_template_view,
        'datatable_view': NotificationTemplateDataTable,
        'verbose_name': 'Notification Template'
    },
    {
        'name': 'booking_source',
        'view_module': booking_source_view,
        'datatable_view': BookingSourceDataTable,
        'verbose_name': 'Booking Source'
    },
    {
        'name': 'country',
        'view_module': country_view,
        'datatable_view': CountryDataTable,
        'verbose_name': 'Country'
    },
    {
        'name': 'printer',
        'view_module': printer_view,
        'datatable_view': PrinterDataTable,
        'verbose_name': 'Printer'
    },
]