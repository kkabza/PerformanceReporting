USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_DTSImport]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_DTSImport](
	[ImportID] [int] IDENTITY(1,1) NOT NULL,
	[VGProductID] [int] NOT NULL,
	[ImportDate] [datetime] NOT NULL,
	[ItemCount] [int] NOT NULL,
	[PaidCount] [int] NULL,
	[UnpaidCount] [int] NULL,
	[UnpaidSum] [decimal](18, 2) NOT NULL,
	[FileName] [varchar](30) NOT NULL,
 CONSTRAINT [PK_vg_DTSImport] PRIMARY KEY CLUSTERED 
(
	[ImportID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
