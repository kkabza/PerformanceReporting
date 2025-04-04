USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_SavedSearchCriteria]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_SavedSearchCriteria](
	[SavedSearchCriteriaID] [int] IDENTITY(1,1) NOT NULL,
	[SavedSearchID] [int] NOT NULL,
	[SearchColumn] [varchar](50) NULL,
	[SearchFunction] [varchar](50) NULL,
	[SearchValue] [varchar](50) NULL,
	[SqlStatement] [varchar](100) NULL,
	[UpdateDate] [datetime] NULL,
 CONSTRAINT [PK_vg_SavedSearchCriteria] PRIMARY KEY CLUSTERED 
(
	[SavedSearchCriteriaID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[vg_SavedSearchCriteria] ADD  CONSTRAINT [DF_vg_SavedSearchCriteria_UpdateDate]  DEFAULT (getdate()) FOR [UpdateDate]
GO
