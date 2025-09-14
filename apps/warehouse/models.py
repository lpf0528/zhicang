import datetime

from django.db import models

from apps.archives.models import Supplier, Customer
from apps.common.models import BaseModel


# Create your models here.


class Warehouse(BaseModel):
    name = models.CharField(max_length=255, verbose_name='仓库名称')
    remark = models.CharField(max_length=255, verbose_name='备注', null=True, blank=True)
    # 负责人
    manager = models.CharField(max_length=255, verbose_name='负责人', null=True, blank=True)
    # 负责人手机号
    manager_phone = models.CharField(max_length=255, verbose_name='负责人手机号', null=True, blank=True)
    # 仓库地址
    address = models.CharField(max_length=255, verbose_name='仓库地址', null=True, blank=True)
    # 仓库电话
    phone = models.CharField(max_length=255, verbose_name='仓库电话', null=True, blank=True)

    class Meta:
        db_table = 'warehouse'
        verbose_name = '仓库'
        verbose_name_plural = '仓库'


class PurchaseOrder(BaseModel):
    class PurchaseTypeChoices(models.TextChoices):
        # 进货/出货
        IN = 'in', '进货'
        OUT = 'out', '出货'

    ticket_no = models.CharField(max_length=255, verbose_name='票号')
    purchase_date = models.DateField(verbose_name='进货日期', default=datetime.date.today)
    type = models.CharField(max_length=10, verbose_name='类型', choices=PurchaseTypeChoices.choices,
                            default=PurchaseTypeChoices.IN)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='仓库')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='供应商')
    operator = models.CharField(max_length=255, verbose_name='经办人', null=True, blank=True)
    settlement_method = models.CharField(max_length=255, verbose_name='结算方式', null=True, blank=True)

    class Meta:
        db_table = 'purchase_order'
        verbose_name = '进货单'
        verbose_name_plural = '进货单'


class PurchaseOrderLine(BaseModel):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, verbose_name='进货单: 可以没有进货单', null=True,
                              blank=True)
    product_model = models.CharField(max_length=255, verbose_name='货品型号', null=True, blank=True)
    product_name = models.CharField(max_length=255, verbose_name='货品名称', null=True, blank=True)
    version = models.CharField(max_length=255, verbose_name='版本：W03/W05', null=True, blank=True)
    spec = models.CharField(max_length=255, verbose_name='规格：2.8米', null=True, blank=True)
    category = models.CharField(max_length=255, verbose_name='货品类别：布/纱/书版', null=True, blank=True)
    unit = models.CharField(max_length=255, verbose_name='单位：米/本/套', null=True, blank=True)
    number = models.IntegerField(verbose_name='原来数量')
    stock_number = models.IntegerField(verbose_name='库存数量', default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='进货单价')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    # status = models.CharField(max_length=255, verbose_name='状态:作废/正常', null=True, blank=True)
    is_revoke = models.BooleanField(verbose_name='是否作废', default=False)
    revoke_reason = models.CharField(max_length=255, verbose_name='作废原因', null=True, blank=True)
    remark = models.CharField(max_length=255, verbose_name='备注', null=True, blank=True)

    class Meta:
        db_table = 'purchase_order_line'
        verbose_name = '进货单明细'
        verbose_name_plural = '进货单明细'


class SaleOrder(BaseModel):
    sale_date = models.DateField(verbose_name='销售日期', default=datetime.date.today)
    no = models.CharField(max_length=255, verbose_name='销售单号: 销202509120001, 可以根据需求量设置长度')
    operator = models.CharField(max_length=255, verbose_name='经办人', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    remark = models.CharField(max_length=255, verbose_name='备注', null=True, blank=True)
    payment_method = models.CharField(max_length=255, verbose_name='收款方式', null=True, blank=True)

    class Meta:
        db_table = 'sale_order'
        verbose_name = '销售单'
        verbose_name_plural = '销售单'


class SaleOrderLine(BaseModel):
    order = models.ForeignKey(SaleOrder, on_delete=models.CASCADE, verbose_name='销售单')
    purchase_order_line = models.ForeignKey(PurchaseOrderLine, on_delete=models.CASCADE, verbose_name='进货单明细')
    number = models.IntegerField(verbose_name='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='销售单价')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='折扣', default=1)
    remark = models.CharField(max_length=255, verbose_name='备注', null=True, blank=True)

    class Meta:
        db_table = 'sale_order_line'
        verbose_name = '销售单明细'
        verbose_name_plural = '销售单明细'
