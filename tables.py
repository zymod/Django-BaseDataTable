class DatatableView(BaseDatatableView):
    fields_excluded = None

    def get_columns(self) -> list:
        if self.fields_excluded:
            return [field.name for field in self.model._meta.fields if field.name not in self.fields_excluded]
        return [field.name for field in self.model._meta.fields]

    def filter_queryset(self, qs) -> QuerySet:
        search_text = self.request.GET.get('search[value]', None)

        if search_text:
            search_terms = search_text.split()
            query = Q()

            for col in self.get_columns():

                field = self.model._meta.get_field(col)
                
                if field.is_relation:
                    if field.many_to_one:
                        and_conditions = [
                            Q(**{f'{col}__name__icontains': term}) for term in search_terms
                        ]

                else:
                    and_conditions = [
                        Q(**{f'{col}__icontains': term}) for term in search_terms
                    ]

                if and_conditions:
                    or_conditions = reduce(and_, and_conditions)
                    query |= or_conditions

            qs = qs.filter(query)
        
        return qs