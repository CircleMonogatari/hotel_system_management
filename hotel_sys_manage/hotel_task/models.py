# Create your models here.

# Create your models here.

manageFlag = True

#
# class Task_config(models.Model):
#     '''
#
#     '''
#     TASK_STATUS = {
#         (0, '等待'),
#         (1, '运行'),
#         (2, '关闭'),
#
#     }
#
#     task_id = models.AutoField(primary_key=True)
#     name = models.CharField('任务名称', max_length=200)
#     task_run_time = models.IntegerField('运行间隔', )
#     task_run_time_out = models.IntegerField('超时等待')
#
#
#     sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
#     sys_update_time = models.DateTimeField('更新时间', auto_now=True)
#     sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
#
#     def __str__(self):
#         return '[{}]-{}'.format(self.countryCn, self.cityCn)
#
#     class Meta:
#         managed = manageFlag
#         verbose_name = '城市信息表'
#         verbose_name_plural = verbose_name
#         db_table = 'city_info'
