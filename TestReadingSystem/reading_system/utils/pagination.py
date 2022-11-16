from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, query_set, page_size=10, page_param="page", plus=3):

        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        page = request.GET.get(page_param, "1")
        self.page_param = page_param
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (self.page - 1) * self.page_size
        self.end = self.page * self.page_size
        self.query_set = query_set[self.start:self.end]
        total_count = query_set.count()
        total_page_count, div = divmod(total_count, self.page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        page_str_list = []
        start_page = max(1, self.page - self.plus)
        end_page = min(self.total_page_count, self.page + self.plus)

        self.query_dict.setlist(self.page_param, [1])
        first = '<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(first)

        self.query_dict.setlist(self.page_param, [self.total_page_count])
        last = '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())

        self.query_dict.setlist(self.page_param, [max(1, self.page - 1)])
        pre = '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'.format(
            self.query_dict.urlencode())
        self.query_dict.setlist(self.page_param, [min(self.total_page_count, self.page + 1)])
        nex = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">»</span></a></li>'.format(
            self.query_dict.urlencode())
        page_str_list.append(pre)
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        page_str_list.append(nex)
        page_str_list.append(last)
        page_string = mark_safe("".join(page_str_list))
        return page_string
