class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'postgres':
            return 'default'
        if model._meta.app_label == 'timescaledb':
            return 'timescaledb'
        if model._meta.app_label == 'supabase':
            return 'supabase'
        return None

    def db_for_write(self, model, **hints):
        return None
    
    # def allow_relation(self, obj1, obj2, **hints):
    #     if obj1._meta.app_label == 'postgres' and obj2._meta.app_label == 'timescaledb':
    #         return True
    #     if obj1._meta.app_label == 'postgres' and obj2._meta.app_label == 'supabase':
    #         return True
    #     if obj1._meta.app_label == 'timescaledb' and obj2._meta.app_label == 'postgres':
    #         return True
    #     if obj1._meta.app_label == 'supabase' and obj2._meta.app_label == 'postgres':
    #         return True
    #     return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return False

